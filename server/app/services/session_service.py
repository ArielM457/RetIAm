from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import run_agent
from app.models.certification import ResourceReference
from app.models.session import (
    EvaluationSubmissionRequest,
    FreeQuestionRequest,
    IntegrityEventRequest,
    LearningSessionResponse,
    MandatoryAnswerRequest,
    SessionQuestion,
    SessionSurveyRequest,
    StartLearningSessionRequest,
)
from app.services import rag_service
from app.services._shared import response_data
from app.services.assessment_service import PASS_THRESHOLD, generate_quiz_questions, grade_lab
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import _get_team_record


def _plan_certification(plan: dict) -> str:
    return plan.get("target_certification", "AZ-900")


def _sanitize_evaluation(evaluation: dict) -> dict:
    """Copia de evaluation sin filtrar las respuestas correctas del quiz al cliente."""
    if not evaluation:
        return {}
    sanitized = dict(evaluation)
    quiz_questions = sanitized.get("quiz_questions")
    if isinstance(quiz_questions, list):
        sanitized["quiz_questions"] = [
            {k: v for k, v in q.items() if k != "correct_option_index"} for q in quiz_questions
        ]
    return sanitized


def _get_plan_for_user(plan_id: str, user_id: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .select("*")
        .eq("id", plan_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=404, detail="Plan no encontrado.")
    return data[0]


def _get_session(session_id: str, user_id: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .select("*")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=404, detail="Sesion no encontrada.")
    return data[0]


def _build_resources(section_title: str) -> list[ResourceReference]:
    return [
        ResourceReference(
            title=f"Resumen de {section_title}",
            type="documentation",
            source=f"{section_title.lower().replace(' ', '-')}-synthetic.md",
            url="https://learn.microsoft.com/",
        ),
        ResourceReference(
            title=f"Ejemplo guiado de {section_title}",
            type="code",
            source=f"{section_title.lower().replace(' ', '-')}-example.md",
            url="https://learn.microsoft.com/training/",
        ),
    ]


def _resolve_learning_style(preferred_format: str | None, session_type: str) -> list[str]:
    if preferred_format:
        normalized = preferred_format.lower()
        if "doc" in normalized or "read" in normalized:
            return ["documentation"]
        if "code" in normalized or "example" in normalized:
            return ["code_examples"]
        if "lab" in normalized or "practice" in normalized or "hands" in normalized:
            return ["hands_on"]
    if session_type in {"lab", "practice"}:
        return ["hands_on"]
    if session_type == "quiz":
        return ["mixed"]
    return ["documentation"]


def _require_mandatory_passed(session: dict) -> None:
    mandatory_answer = (session.get("evaluation") or {}).get("mandatory_answer") or {}
    if not mandatory_answer:
        raise HTTPException(status_code=409, detail="Debes responder la pregunta obligatoria antes de evaluar la sesion.")
    if not mandatory_answer.get("is_correct"):
        raise HTTPException(
            status_code=409,
            detail="No puedes avanzar hasta responder correctamente la pregunta obligatoria.",
        )


def start_learning_session(auth_user: object, payload: StartLearningSessionRequest) -> LearningSessionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    plan = _get_plan_for_user(payload.plan_id, profile.id)
    certification = _plan_certification(plan)

    resources = _build_resources(payload.section_title)
    mandatory_question = SessionQuestion(
        prompt=f"Explica el concepto central de {payload.section_title} con tus propias palabras.",
        answer=f"El concepto central de {payload.section_title} debe vincularse con el objetivo de la certificacion y la practica del modulo.",
        source=resources[0].source,
    )

    # Para teoria/quiz generamos un quiz real (Gini Eval o banco) calificado en servidor.
    initial_evaluation: dict = {}
    if payload.session_type in {"theory", "quiz"}:
        quiz_questions, quiz_source_mode = generate_quiz_questions(
            certification, payload.section_title, None, n=4, section_id=payload.section_id
        )
        initial_evaluation = {
            "quiz_questions": quiz_questions,
            "quiz_source_mode": quiz_source_mode,
        }

    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .insert(
            {
                "user_id": profile.id,
                "plan_id": payload.plan_id,
                "section_id": payload.section_id,
                "section_title": payload.section_title,
                "session_type": payload.session_type,
                "status": "in_progress",
                "resources": [item.model_dump() for item in resources],
                "mandatory_question": mandatory_question.model_dump(),
                "free_questions": [],
                "evaluation": initial_evaluation,
            }
        )
        .execute()
    )
    data = response_data(response, [])[0]
    return LearningSessionResponse(
        id=data["id"],
        plan_id=data["plan_id"],
        section_id=data["section_id"],
        section_title=data["section_title"],
        session_type=data["session_type"],
        status=data["status"],
        resources=resources,
        mandatory_question=mandatory_question,
        free_questions=[],
        evaluation=_sanitize_evaluation(data.get("evaluation") or {}),
        started_at=data["started_at"],
        completed_at=data.get("completed_at"),
    )


def get_learning_session(auth_user: object, session_id: str) -> LearningSessionResponse:
    profile = ensure_profile_for_user(auth_user)
    data = _get_session(session_id, profile.id)
    return LearningSessionResponse(
        id=data["id"],
        plan_id=data["plan_id"],
        section_id=data["section_id"],
        section_title=data["section_title"],
        session_type=data["session_type"],
        status=data["status"],
        resources=[ResourceReference.model_validate(item) for item in data["resources"]],
        mandatory_question=SessionQuestion.model_validate(data["mandatory_question"])
        if data.get("mandatory_question")
        else None,
        free_questions=data.get("free_questions") or [],
        evaluation=_sanitize_evaluation(data.get("evaluation") or {}),
        survey=data.get("survey"),
        started_at=data.get("started_at"),
        completed_at=data.get("completed_at"),
    )


def submit_mandatory_answer(auth_user: object, session_id: str, payload: MandatoryAnswerRequest) -> LearningSessionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    session = _get_session(session_id, profile.id)
    question = session.get("mandatory_question") or {}
    expected = (question.get("answer") or "").lower()
    submitted = payload.answer.lower()
    is_correct = any(token in submitted for token in expected.split()[:4]) if expected else False
    evaluation = session.get("evaluation") or {}
    evaluation["mandatory_answer"] = {
        "submitted_answer": payload.answer,
        "is_correct": is_correct,
        "feedback": (
            "Respuesta aceptada para continuar."
            if is_correct
            else "La respuesta no demuestra suficiente dominio. Revisa el recurso principal y vuelve a intentar."
        ),
    }
    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .update({"evaluation": evaluation, "status": "in_progress" if is_correct else "needs_retry"})
        .eq("id", session_id)
        .execute()
    )
    return get_learning_session(auth_user, response_data(response, [])[0]["id"])


def answer_free_question(auth_user: object, session_id: str, payload: FreeQuestionRequest) -> LearningSessionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    session = _get_session(session_id, profile.id)
    section_title = session.get("section_title", "el modulo actual")
    plan = _get_plan_for_user(session["plan_id"], profile.id)
    certification = _plan_certification(plan)

    # Fundamentado con RAG (mismo mecanismo que el tutor por leccion).
    chunks = rag_service.retrieve(certification, payload.question, k=5)
    source = (chunks[0].get("source_url") if chunks else None) or "rag"

    if chunks:
        context_text = "\n\n".join(c.get("content", "") for c in chunks)
        prompt = (
            f"Responde la duda del alumno sobre «{section_title}» USANDO SOLO el contexto del "
            "curso. Si no está en el contexto, dilo y no inventes.\n\n"
            f"CONTEXTO:\n{context_text}\n\nPregunta: {payload.question}\n\n"
            "Responde en español, claro y conciso (máx 150 palabras)."
        )
        result = run_agent("gini-eval", prompt, temperature=0.2, max_tokens=500, ground=False)
        if result:
            answer_text = result["text"]
            source_mode = "foundry"
        else:
            top = chunks[0].get("content", "")
            answer_text = f"Según el material del curso:\n\n{top[:500]}" + ("…" if len(top) > 500 else "")
            source_mode = "mock"
    else:
        answer_text = (
            "No encuentro material indexado para responder esa pregunta con seguridad. "
            "Revisa las fuentes oficiales de la sección."
        )
        source_mode = "mock"

    free_questions = session.get("free_questions") or []
    free_questions.append(
        {
            "question": payload.question,
            "answer": answer_text,
            "source": source,
            "source_mode": source_mode,
        }
    )
    get_supabase_service_client().table(settings.supabase_learning_sessions_table).update(
        {"free_questions": free_questions}
    ).eq("id", session_id).execute()
    return get_learning_session(auth_user, session_id)


def submit_session_evaluation(auth_user: object, session_id: str, payload: EvaluationSubmissionRequest) -> LearningSessionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    session = _get_session(session_id, profile.id)
    _require_mandatory_passed(session)
    evaluation = session.get("evaluation") or {}

    if payload.lab_solution_summary:
        lab_result = grade_lab(
            session.get("section_title", "la seccion"),
            instructions=None,
            solution_summary=payload.lab_solution_summary,
            rubric=None,
        )
        passed = lab_result["passed"]
        evaluation["lab"] = lab_result
    else:
        quiz_questions = evaluation.get("quiz_questions") or []
        correct_by_id = {q["question_id"]: q.get("correct_option_index") for q in quiz_questions}
        submitted = payload.quiz_answers or []
        if not submitted and payload.answers:
            # Compat: aceptar [{question_id, selected_option_index}] en answers.
            submitted = [
                type("A", (), {"question_id": a.get("question_id"), "selected_option_index": a.get("selected_option_index")})()
                for a in payload.answers
                if a.get("question_id") is not None and a.get("selected_option_index") is not None
            ]
        if quiz_questions:
            total = len(quiz_questions)
            correct = sum(
                1
                for answer in submitted
                if correct_by_id.get(answer.question_id) == answer.selected_option_index
            )
        else:
            # Sin banco almacenado: no se puede calificar de forma confiable.
            total = max(1, len(submitted))
            correct = 0
        score = int((correct / max(1, total)) * 100)
        passed = score >= PASS_THRESHOLD
        evaluation["quiz"] = {
            "score": score,
            "passed": passed,
            "total_questions": total,
            "correct_answers": correct,
            "source_mode": evaluation.get("quiz_source_mode", "mock"),
        }

    completed_at = datetime.now(timezone.utc).isoformat() if passed else None
    get_supabase_service_client().table(settings.supabase_learning_sessions_table).update(
        {
            "evaluation": evaluation,
            "status": "completed" if passed else "needs_retry",
            "completed_at": completed_at,
        }
    ).eq("id", session_id).execute()
    return get_learning_session(auth_user, session_id)


def submit_session_survey(auth_user: object, session_id: str, payload: SessionSurveyRequest) -> LearningSessionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    session = _get_session(session_id, profile.id)
    if not payload.skipped and (payload.clarity_score is None or not payload.preferred_format):
        raise HTTPException(
            status_code=400,
            detail="Si no saltas la encuesta, debes enviar claridad y formato preferido.",
        )

    survey = payload.model_dump(exclude_none=True)
    inferred_style = _resolve_learning_style(payload.preferred_format, session["session_type"])
    survey["inferred_learning_style"] = inferred_style
    get_supabase_service_client().table(settings.supabase_learning_sessions_table).update(
        {"survey": survey}
    ).eq("id", session_id).execute()

    profile_record_response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .select("learning_style, profile_version")
        .eq("id", profile.id)
        .limit(1)
        .execute()
    )
    profile_record = (response_data(profile_record_response, []) or [None])[0] or {}
    current_styles = list(profile_record.get("learning_style") or [])
    updated_styles = current_styles if payload.skipped else list(dict.fromkeys(inferred_style + current_styles))
    get_supabase_service_client().table(settings.supabase_profiles_table).update(
        {
            "learning_style": updated_styles[:4],
            "profile_version": int(profile_record.get("profile_version") or 1) + 1,
        }
    ).eq("id", profile.id).execute()
    return get_learning_session(auth_user, session_id)


def record_integrity_event(auth_user: object, session_id: str, payload: IntegrityEventRequest) -> dict:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    session = _get_session(session_id, profile.id)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_integrity_events_table)
        .insert(
            {
                "session_id": session_id,
                "user_id": profile.id,
                "event_type": payload.event_type,
                "payload": payload.payload,
            }
        )
        .execute()
    )
    event_data = response_data(response, [])[0]

    plan_response = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .select("*")
        .eq("id", session["plan_id"])
        .limit(1)
        .execute()
    )
    plan = (response_data(plan_response, []) or [None])[0]
    manager_notification = None
    if plan:
        team_assignment_response = (
            get_supabase_service_client()
            .table(settings.supabase_team_cert_assignments_table)
            .select("*")
            .contains("member_ids", [profile.id])
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        assignment = (response_data(team_assignment_response, []) or [None])[0]
        if assignment:
            team = _get_team_record(assignment["team_id"])
            manager_notification = {
                "manager_id": team["manager_id"],
                "team_id": team["id"],
                "message": (
                    f"Se detecto un evento de integridad {payload.event_type} en la sesion {session['section_title']} "
                    f"del usuario {profile.full_name or profile.email}."
                ),
            }
            get_supabase_service_client().table(settings.supabase_coach_reminders_table).insert(
                {
                    "user_id": team["manager_id"],
                    "plan_id": None,
                    "kind": "standard",
                    "tone": "concise",
                    "delivery_channel": "platform",
                    "message": manager_notification["message"],
                    "scheduled_for": datetime.now(timezone.utc).isoformat(),
                    "status": "scheduled",
                }
            ).execute()

    return {
        **event_data,
        "manager_notified": bool(manager_notification),
        "manager_notification": manager_notification,
    }
