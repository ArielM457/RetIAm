from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.onboarding import (
    LearningProfileSnapshot,
    OnboardingAnswerResult,
    OnboardingEvaluationRequest,
    OnboardingEvaluationResponse,
    OnboardingQuestion,
    OnboardingQuestionOption,
    OnboardingQuestionsResponse,
    SavedAssessmentResponse,
)
from app.services._shared import response_data
from app.services.onboarding_catalog import CERTIFICATION_TRACK_HINTS, QUESTION_BANK
from app.services.profile_service import ensure_profile_for_user


def _resolve_track(target_certification: str) -> str:
    if target_certification in CERTIFICATION_TRACK_HINTS:
        return CERTIFICATION_TRACK_HINTS[target_certification]

    normalized = target_certification.lower()
    if "aws" in normalized:
        return "aws"
    if "github" in normalized:
        return "github"
    return "azure"


def get_onboarding_questions(target_certification: str) -> OnboardingQuestionsResponse:
    track = _resolve_track(target_certification)
    questions = [
        OnboardingQuestion(
            id=item["id"],
            prompt=item["prompt"],
            topic=item["topic"],
            difficulty=item["difficulty"],
            options=[OnboardingQuestionOption.model_validate(option) for option in item["options"]],
        )
        for item in QUESTION_BANK[track]
    ]
    return OnboardingQuestionsResponse(
        track=track,
        target_certification=target_certification,
        questions=questions,
    )


def _build_question_map(track: str) -> dict[str, dict]:
    return {item["id"]: item for item in QUESTION_BANK[track]}


def _detect_level(answer_results: list[OnboardingAnswerResult], score: int, max_score: int) -> str:
    if not answer_results or max_score <= 0:
        return "basic"

    basic_wrong = any(
        result.difficulty == "basic" and not result.is_correct for result in answer_results
    )
    ratio = score / max_score
    if basic_wrong and ratio < 0.7:
        return "basic"
    if ratio >= 0.8:
        return "advanced"
    if ratio >= 0.45:
        return "intermediate"
    return "basic"


def _build_summary(level: str, payload: OnboardingEvaluationRequest) -> tuple[str, list[str]]:
    summaries = {
        "basic": (
            "Detectamos una base inicial. Conviene empezar con fundamentos claros y sesiones cortas para construir confianza.",
            [
                "Arranca por conceptos base de la certificacion antes de labs complejos.",
                "Usa sesiones frecuentes de 30 a 45 minutos para sostener ritmo.",
                "Prioriza recursos guiados y ejemplos explicados paso a paso.",
            ],
        ),
        "intermediate": (
            "Detectamos un nivel intermedio. Ya puedes avanzar con una ruta balanceada entre teoria y practica.",
            [
                "Alterna documentacion con ejercicios aplicados en cada semana.",
                "Reserva bloques fijos para reforzar los temas donde dudaste.",
                "Apunta a una certificacion con hitos semanales claros y medibles.",
            ],
        ),
        "advanced": (
            "Detectamos un nivel avanzado. Puedes trabajar con una ruta mas acelerada y enfocada en vacios puntuales.",
            [
                "Prioriza simulaciones, quizzes y laboratorios de validacion.",
                "Reduce tiempo en fundamentos y enfoca el plan en brechas especificas.",
                "Aprovecha mas horas por semana para acercar la fecha objetivo.",
            ],
        ),
    }
    summary, recommendations = summaries[level]
    recommendations = recommendations + [
        f"Preferencia horaria declarada: {payload.preferred_time}.",
        f"Estilo de aprendizaje declarado: {', '.join(payload.learning_style)}.",
    ]
    return summary, recommendations


def evaluate_onboarding(auth_user: object, payload: OnboardingEvaluationRequest) -> OnboardingEvaluationResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    track = _resolve_track(payload.target_certification)
    question_map = _build_question_map(track)

    if len(payload.answers) > len(question_map):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se enviaron mas respuestas que preguntas disponibles para esta evaluacion.",
        )

    answer_results: list[OnboardingAnswerResult] = []
    score = 0
    max_score = 0
    seen_ids: set[str] = set()
    difficulty_points = {"basic": 1, "intermediate": 2, "advanced": 3}

    for answer in payload.answers:
        if answer.question_id in seen_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se permiten preguntas repetidas en la evaluacion inicial.",
            )
        seen_ids.add(answer.question_id)

        question = question_map.get(answer.question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La pregunta {answer.question_id} no pertenece al track {track}.",
            )

        points = difficulty_points[question["difficulty"]]
        max_score += points
        is_correct = answer.selected_option_key == question["correct_option_key"]
        if is_correct:
            score += points

        answer_results.append(
            OnboardingAnswerResult(
                question_id=answer.question_id,
                selected_option_key=answer.selected_option_key,
                correct_option_key=question["correct_option_key"],
                is_correct=is_correct,
                difficulty=question["difficulty"],
                topic=question["topic"],
            )
        )

    level = _detect_level(answer_results, score, max_score)
    summary, recommendations = _build_summary(level, payload)
    completed_at = datetime.now(timezone.utc).isoformat()

    current_version = getattr(profile, "profile_version", 1) if hasattr(profile, "profile_version") else 1
    next_version = current_version + 1
    profile_update = {
        "professional_role": payload.professional_role,
        "target_certification": payload.target_certification,
        "detected_level": level,
        "weekly_hours_available": payload.weekly_hours_available,
        "preferred_time": payload.preferred_time,
        "learning_style": payload.learning_style,
        "profile_version": next_version,
        "onboarding_completed_at": completed_at,
    }

    get_supabase_service_client().table(settings.supabase_profiles_table).update(profile_update).eq(
        "id", profile.id
    ).execute()

    assessment_payload = {
        "user_id": profile.id,
        "professional_role": payload.professional_role,
        "target_certification": payload.target_certification,
        "detected_level": level,
        "weekly_hours_available": payload.weekly_hours_available,
        "preferred_time": payload.preferred_time,
        "learning_style": payload.learning_style,
        "questions": [question_map[result.question_id] for result in answer_results],
        "answers": [result.model_dump() for result in answer_results],
        "score": score,
        "max_score": max_score,
        "notes": summary,
    }
    get_supabase_service_client().table(settings.supabase_profile_assessments_table).insert(
        assessment_payload
    ).execute()

    return OnboardingEvaluationResponse(
        profile=LearningProfileSnapshot(
            professional_role=payload.professional_role,
            target_certification=payload.target_certification,
            detected_level=level,
            weekly_hours_available=payload.weekly_hours_available,
            preferred_time=payload.preferred_time,
            learning_style=payload.learning_style,
            profile_version=next_version,
            onboarding_completed_at=completed_at,
        ),
        score=score,
        max_score=max_score,
        answer_results=answer_results,
        summary=summary,
        recommendations=recommendations,
    )


def get_latest_assessment(auth_user: object) -> SavedAssessmentResponse | None:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_profile_assessments_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        return None
    return SavedAssessmentResponse.model_validate(data[0])
