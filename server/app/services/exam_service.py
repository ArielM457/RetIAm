from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.exam import (
    CertificateResponse,
    ExamQuestion,
    FinalExamAttemptResponse,
    StartFinalExamRequest,
    SubmitFinalExamRequest,
)
from app.services._shared import response_data
from app.services.pdf_service import generate_simple_pdf
from app.services.profile_service import ensure_profile_for_user


def _build_exam_questions(route: dict) -> list[ExamQuestion]:
    sections = route["sections"]
    target_questions = min(25, max(15, len(sections) * 5))
    total_hours = sum(section["estimated_hours"] for section in sections) or len(sections)
    allocations = []
    assigned = 0
    for section in sections:
        proportional = max(1, round((section["estimated_hours"] / total_hours) * target_questions))
        allocations.append(proportional)
        assigned += proportional

    while assigned > target_questions:
        for index, value in enumerate(allocations):
            if value > 1 and assigned > target_questions:
                allocations[index] -= 1
                assigned -= 1
    while assigned < target_questions:
        for index in range(len(allocations)):
            if assigned < target_questions:
                allocations[index] += 1
                assigned += 1

    questions: list[ExamQuestion] = []
    question_number = 1
    for section, amount in zip(sections, allocations, strict=False):
        for section_index in range(amount):
            questions.append(
                ExamQuestion(
                    question_id=f"exam-{question_number}",
                    prompt=f"Pregunta {question_number} sobre {section['title']} enfocada en el criterio {section_index + 1}.",
                    options=["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
                    correct_option_index=(section_index % 4),
                    source=section["resources"][0]["source"],
                    section_id=section["section_id"],
                )
            )
            question_number += 1
    return questions


def _next_certification(current_certification: str) -> str | None:
    progression = {
        "AZ-900": "AZ-204",
        "AZ-204": "AZ-305",
        "AWS Cloud Practitioner": "AWS Solutions Architect Associate",
        "GitHub Foundations": "GitHub Actions",
    }
    return progression.get(current_certification)


def _build_failure_recommendations(failed_sections: list[str]) -> list[str]:
    recommendations = [
        f"Refuerza la seccion {section} con una sesion guiada y un quiz de repaso antes de reintentar."
        for section in failed_sections
    ]
    recommendations.append("Programa un nuevo intento solo despues de cerrar las secciones con mayor error.")
    return recommendations


def start_final_exam(auth_user: object, payload: StartFinalExamRequest) -> FinalExamAttemptResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    plan_response = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .select("*")
        .eq("id", payload.plan_id)
        .eq("user_id", profile.id)
        .limit(1)
        .execute()
    )
    plan = (response_data(plan_response, []) or [None])[0]
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado.")

    route_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_routes_table)
        .select("*")
        .eq("id", plan["route_id"])
        .limit(1)
        .execute()
    )
    route = (response_data(route_response, []) or [None])[0]
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada.")
    session_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .select("section_id,status")
        .eq("plan_id", payload.plan_id)
        .eq("user_id", profile.id)
        .execute()
    )
    completed_sections = {
        item["section_id"] for item in (response_data(session_response, []) or []) if item.get("status") == "completed"
    }
    route_sections = {section["section_id"] for section in route["sections"]}
    if route_sections - completed_sections:
        raise HTTPException(
            status_code=409,
            detail="Debes completar todas las secciones del plan antes de iniciar el examen final.",
        )

    questions = _build_exam_questions(route)
    time_limit_minutes = payload.time_limit_minutes
    response = (
        get_supabase_service_client()
        .table(settings.supabase_exam_attempts_table)
        .insert(
            {
                "user_id": profile.id,
                "plan_id": payload.plan_id,
                "target_certification": plan["target_certification"],
                "questions": [item.model_dump() for item in questions],
                "answers": [],
                "score": 0,
                "max_score": 100,
                "passed": False,
                "time_limit_minutes": time_limit_minutes,
                "failed_sections": [],
                "recommendations": [],
                "next_certification": _next_certification(plan["target_certification"]),
            }
        )
        .execute()
    )
    data = response_data(response, [])[0]
    return FinalExamAttemptResponse(
        id=data["id"],
        plan_id=data["plan_id"],
        target_certification=data["target_certification"],
        questions=questions,
        time_limit_minutes=data.get("time_limit_minutes", time_limit_minutes),
        score=data["score"],
        max_score=data["max_score"],
        passed=data["passed"],
        failed_sections=data.get("failed_sections") or [],
        recommendations=data.get("recommendations") or [],
        next_certification=data.get("next_certification"),
        started_at=data["started_at"],
        submitted_at=data.get("submitted_at"),
    )


def submit_final_exam(auth_user: object, attempt_id: str, payload: SubmitFinalExamRequest) -> FinalExamAttemptResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    attempt_response = (
        get_supabase_service_client()
        .table(settings.supabase_exam_attempts_table)
        .select("*")
        .eq("id", attempt_id)
        .eq("user_id", profile.id)
        .limit(1)
        .execute()
    )
    attempt = (response_data(attempt_response, []) or [None])[0]
    if not attempt:
        raise HTTPException(status_code=404, detail="Intento no encontrado.")
    questions = [ExamQuestion.model_validate(item) for item in attempt["questions"]]
    started_at_dt = datetime.fromisoformat(attempt["started_at"].replace("Z", "+00:00"))
    time_limit_minutes = int(attempt.get("time_limit_minutes") or 60)
    if datetime.now(timezone.utc) > started_at_dt + timedelta(minutes=time_limit_minutes):
        raise HTTPException(status_code=409, detail="El tiempo limite del examen ya expiro.")
    correct = 0
    answers_by_question = {answer.get("question_id"): answer for answer in payload.answers}
    failed_section_ids: list[str] = []
    for question in questions:
        answer = answers_by_question.get(question.question_id)
        if answer and answer.get("selected_option_index") == question.correct_option_index:
            correct += 1
        elif question.section_id not in failed_section_ids:
            failed_section_ids.append(question.section_id)
    score_percent = int((correct / max(1, len(questions))) * 100)
    passed = score_percent >= 70
    submitted_at = datetime.now(timezone.utc).isoformat()
    failed_sections = sorted({question.section_id for question in questions if question.section_id in failed_section_ids})
    recommendations = [] if passed else _build_failure_recommendations(failed_sections)
    next_certification = _next_certification(attempt["target_certification"]) if passed else None
    certificate_id = None
    get_supabase_service_client().table(settings.supabase_exam_attempts_table).update(
        {
            "answers": payload.answers,
            "score": score_percent,
            "max_score": 100,
            "passed": passed,
            "submitted_at": submitted_at,
            "failed_sections": failed_sections,
            "recommendations": recommendations,
            "next_certification": next_certification,
        }
    ).eq("id", attempt_id).execute()

    if passed:
        certificate_id = f"CERT-{attempt['target_certification'].replace(' ', '').upper()}-{profile.id[:8]}-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
        verification_code = str(uuid4())[:8].upper()
        pdf_path = Path(__file__).resolve().parents[2] / "generated" / "certificates" / f"{certificate_id}.pdf"
        generate_simple_pdf(
            pdf_path,
            "Certificado RetAIM",
            [
                f"Participante: {profile.full_name or 'Usuario demo'}",
                f"Certificacion: {attempt['target_certification']}",
                f"Puntaje final: {score_percent}",
                f"Fecha: {submitted_at[:10]}",
                f"Codigo de verificacion: {verification_code}",
            ],
        )
        get_supabase_service_client().table(settings.supabase_certificates_table).upsert(
            {
                "id": certificate_id,
                "user_id": profile.id,
                "recipient_name": profile.full_name or "Usuario demo",
                "target_certification": attempt["target_certification"],
                "score": score_percent,
                "pdf_url": f"/generated/certificates/{certificate_id}.pdf",
                "verification_code": verification_code,
            }
        ).execute()
    else:
        get_supabase_service_client().table(settings.supabase_study_plans_table).update(
            {"status": "needs_reinforcement"}
        ).eq("id", attempt["plan_id"]).execute()
    return FinalExamAttemptResponse(
        id=attempt_id,
        plan_id=attempt["plan_id"],
        target_certification=attempt["target_certification"],
        questions=questions,
        time_limit_minutes=time_limit_minutes,
        score=score_percent,
        max_score=100,
        passed=passed,
        failed_sections=failed_sections,
        recommendations=recommendations,
        next_certification=next_certification,
        certificate_id=certificate_id,
        started_at=attempt["started_at"],
        submitted_at=submitted_at,
    )


def list_my_certificates(auth_user: object) -> list[CertificateResponse]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_certificates_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("issued_at", desc=True)
        .execute()
    )
    return [CertificateResponse.model_validate(item) for item in (response_data(response, []) or [])]
