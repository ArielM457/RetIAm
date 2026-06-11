import re
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.onboarding import (
    AgentIntakeAssistRequest,
    AgentIntakeAssistResponse,
    AgentIntakeRequest,
    AgentIntakeResponse,
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

DAY_ALIASES = {
    "lunes": "Monday",
    "monday": "Monday",
    "martes": "Tuesday",
    "tuesday": "Tuesday",
    "miercoles": "Wednesday",
    "miércoles": "Wednesday",
    "wednesday": "Wednesday",
    "jueves": "Thursday",
    "thursday": "Thursday",
    "viernes": "Friday",
    "friday": "Friday",
    "sabado": "Saturday",
    "sábado": "Saturday",
    "saturday": "Saturday",
    "domingo": "Sunday",
    "sunday": "Sunday",
}


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
            preferred_start_hour=getattr(payload, "preferred_start_hour", None),
            preferred_study_days=list(getattr(payload, "preferred_study_days", []) or []),
            learning_style=payload.learning_style,
            content_preferences=list(getattr(payload, "content_preferences", []) or []),
            study_techniques=list(getattr(payload, "study_techniques", []) or []),
            learning_goals=list(getattr(payload, "learning_goals", []) or []),
            technology_experience=list(getattr(payload, "technology_experience", []) or []),
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
    try:
        response = (
            get_supabase_service_client()
            .table(settings.supabase_profile_assessments_table)
            .select("*")
            .eq("user_id", profile.id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception:
        return None
    data = response_data(response, [])
    if not data:
        return None
    try:
        return SavedAssessmentResponse.model_validate(data[0])
    except Exception:
        return None


def save_agent_intake(auth_user: object, payload: AgentIntakeRequest) -> AgentIntakeResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    completed_at = datetime.now(timezone.utc).isoformat()
    current_version = getattr(profile, "profile_version", 1) if hasattr(profile, "profile_version") else 1
    next_version = current_version + 1

    summary = (
        f"Perfil inicial registrado para {payload.professional_role}. "
        f"Disponibilidad estimada: {payload.weekly_hours_available} horas por semana, "
        f"preferencia horaria {payload.preferred_time} desde las {payload.preferred_start_hour}:00, "
        f"con estudio en {', '.join(payload.preferred_study_days)} y estilos {', '.join(payload.learning_style)}."
    )

    get_supabase_service_client().table(settings.supabase_profiles_table).update(
        {
            "professional_role": payload.professional_role,
            "weekly_hours_available": payload.weekly_hours_available,
            "preferred_time": payload.preferred_time,
            "preferred_start_hour": payload.preferred_start_hour,
            "preferred_study_days": payload.preferred_study_days,
            "learning_style": payload.learning_style,
            "content_preferences": payload.content_preferences,
            "study_techniques": payload.study_techniques,
            "learning_goals": payload.learning_goals,
            "technology_experience": payload.technology_experience,
            "target_certification": payload.target_certification,
            "profile_version": next_version,
            "onboarding_completed_at": completed_at,
        }
    ).eq("id", profile.id).execute()

    get_supabase_service_client().table(settings.supabase_profile_assessments_table).insert(
        {
            "user_id": profile.id,
            "professional_role": payload.professional_role,
            "target_certification": payload.target_certification or "pending",
            "detected_level": "basic",
            "weekly_hours_available": payload.weekly_hours_available,
            "preferred_time": payload.preferred_time,
            "preferred_start_hour": payload.preferred_start_hour,
            "preferred_study_days": payload.preferred_study_days,
            "learning_style": payload.learning_style,
            "content_preferences": payload.content_preferences,
            "study_techniques": payload.study_techniques,
            "learning_goals": payload.learning_goals,
            "technology_experience": payload.technology_experience,
            "questions": [
                {"key": answer.key, "title": answer.title}
                for answer in payload.answers
            ],
            "answers": [answer.model_dump() for answer in payload.answers],
            "score": 0,
            "max_score": 0,
            "notes": summary,
        }
    ).execute()

    return AgentIntakeResponse(
        summary=summary,
        saved_answers=len(payload.answers),
        onboarding_completed_at=completed_at,
    )


def _extract_weekly_hours(message: str) -> str | None:
    digits = "".join(char for char in message if char.isdigit())
    if not digits:
        return None
    return str(max(1, min(60, int(digits))))


def _extract_preferred_time(message: str) -> str | None:
    lowered = message.lower()
    if any(token in lowered for token in ("morning", "mañana", "manana", "temprano")):
        return "morning"
    if any(token in lowered for token in ("afternoon", "tarde", "mediodia", "medio día")):
        return "afternoon"
    if any(token in lowered for token in ("night", "noche", "nights")):
        return "night"
    return None


def _extract_preferred_start_hour(message: str, preferred_time: str | None = None) -> int | None:
    lowered = message.lower().replace(".", ":")
    matches = re.findall(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", lowered)
    if not matches:
        return None

    for hour_text, _minute, meridiem in matches:
        hour = int(hour_text)
        if meridiem == "pm" and hour < 12:
            hour += 12
        elif meridiem == "am" and hour == 12:
            hour = 0
        elif meridiem is None and preferred_time == "night" and 6 <= hour <= 11:
            hour += 12
        elif meridiem is None and preferred_time == "afternoon" and 1 <= hour <= 7:
            hour += 12
        if 0 <= hour <= 23:
            return hour
    return None


def _extract_preferred_study_days(message: str) -> list[str]:
    lowered = message.lower()
    if "lunes a viernes" in lowered or "monday to friday" in lowered:
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    if "lunes a domingo" in lowered or "monday to sunday" in lowered:
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    found: list[str] = []
    for token, canonical in DAY_ALIASES.items():
        if re.search(rf"\b{re.escape(token)}\b", lowered):
            found.append(canonical)
    return list(dict.fromkeys(found))


def _extract_learning_style(message: str) -> str | None:
    lowered = message.lower()
    matches: list[str] = []
    if any(token in lowered for token in ("video", "videos", "visual")):
        matches.append("video")
    if any(token in lowered for token in ("texto", "textos", "documentacion", "documentación", "lectura")):
        matches.append("textos")
    if any(token in lowered for token in ("practica", "práctica", "hands-on", "laboratorio", "lab")):
        matches.append("practica")
    if any(token in lowered for token in ("codigo", "código", "ejemplos")):
        matches.append("codigo")
    if "mixto" in lowered or "mixed" in lowered:
        matches.append("mixto")
    if not matches:
        return None
    unique_matches = list(dict.fromkeys(matches))
    return ", ".join(unique_matches)


def _extract_age_range(message: str) -> str | None:
    range_match = re.search(r"(\d{2})\s*[-a]\s*(\d{2})", message)
    if range_match:
        return f"{range_match.group(1)}-{range_match.group(2)}"
    digits = _extract_weekly_hours(message)
    if not digits:
        return None
    age = int(digits)
    if 18 <= age <= 24:
        return "18-24"
    if 25 <= age <= 34:
        return "25-34"
    if 35 <= age <= 44:
        return "35-44"
    if 45 <= age <= 54:
        return "45-54"
    if age >= 55:
        return "55+"
    return None


def _extract_study_techniques(message: str) -> str | None:
    lowered = message.lower()
    matches: list[str] = []
    if "pomodoro" in lowered:
        matches.append("pomodoro")
    if "5 minutos" in lowered or "5 minute" in lowered:
        matches.append("regla de 5 minutos")
    if "continuo" in lowered or "continuo" in lowered or "aprendizaje continuo" in lowered:
        matches.append("aprendizaje continuo")
    if "feynman" in lowered:
        matches.append("feynman")
    if "espaciad" in lowered or "spaced repetition" in lowered:
        matches.append("repeticion espaciada")
    if "recall" in lowered or "active recall" in lowered:
        matches.append("active recall")
    if "intercalad" in lowered or "interleaving" in lowered:
        matches.append("intercalado")
    if not matches:
        return None
    return ", ".join(dict.fromkeys(matches))


def assist_agent_intake(auth_user: object, payload: AgentIntakeAssistRequest) -> AgentIntakeAssistResponse:
    ensure_profile_for_user(auth_user)
    message = payload.user_message.strip()
    lowered = message.lower()
    extracted_answers: dict[str, str] = {}

    weekly_hours = _extract_weekly_hours(message)
    preferred_time = _extract_preferred_time(message)
    preferred_start_hour = _extract_preferred_start_hour(message, preferred_time)
    preferred_study_days = _extract_preferred_study_days(message)
    learning_style = _extract_learning_style(message)
    age_range = _extract_age_range(message)
    study_techniques = _extract_study_techniques(message)

    if weekly_hours:
        extracted_answers["weekly_hours_available"] = weekly_hours
    if preferred_time:
        extracted_answers["preferred_time"] = preferred_time
    if preferred_start_hour is not None:
        extracted_answers["preferred_start_hour"] = str(preferred_start_hour)
    if preferred_study_days:
        extracted_answers["preferred_study_days"] = ", ".join(preferred_study_days)
    if learning_style:
        extracted_answers["learning_style"] = learning_style
    if age_range:
        extracted_answers["age_range"] = age_range
    if study_techniques:
        extracted_answers["study_techniques"] = study_techniques

    if "?" in message or lowered.startswith(("que ", "qué ", "como ", "cómo ", "cual ", "cuál ", "puedo ", "debo ")):
        help_map = {
            "professional_role": "Puedes responder con tu puesto real o el rol con el que trabajas hoy en el equipo.",
            "age_range": "Si no quieres decir la edad exacta, basta con un rango como 25-34 o 35-44.",
            "weekly_hours_available": "Aqui necesito una estimacion realista de horas por semana para estudiar.",
            "preferred_time": "En este mismo paso define bloque y hora, por ejemplo night desde las 8 pm o mañana desde las 7 am.",
            "preferred_study_days": "Puedes elegir patrones como lunes a viernes, lunes miercoles y viernes o martes jueves y sabado.",
            "learning_style": "Puedes combinar formatos como video, textos, practica o ejemplos de codigo.",
            "content_preferences": "Aqui sirve una frase corta como laboratorios reales, casos de uso, resúmenes o guias paso a paso.",
            "technology_experience": "Aqui me sirve una lista breve de tecnologias que ya usas o has probado.",
            "learning_goals": "Aqui puedes contar que te gustaria aprender o mejorar primero.",
            "study_techniques": "Aqui puedes mencionar pomodoro, regla de 5 minutos, aprendizaje continuo, feynman o repeticion espaciada.",
        }
        return AgentIntakeAssistResponse(
            message=f"{help_map.get(payload.question_key, 'Voy a ayudarte solo con este paso del perfil inicial.')} Cuando quieras, responde este paso: {payload.question_title}.",
            extracted_answers=extracted_answers,
        )

    normalized_answer = message
    if payload.question_key == "weekly_hours_available":
        if weekly_hours:
            normalized_answer = weekly_hours
        else:
            return AgentIntakeAssistResponse(
                message="Para este paso necesito una cantidad aproximada de horas. Puedes responder algo como 4, 6 u 8.",
                extracted_answers=extracted_answers,
            )
    elif payload.question_key == "preferred_time":
        if preferred_time and preferred_start_hour is not None:
            normalized_answer = f"{preferred_time} desde las {preferred_start_hour:02d}:00"
        else:
            return AgentIntakeAssistResponse(
                message="Para este paso necesito bloque y hora exacta. Puedes responder algo como night desde las 8 pm.",
                extracted_answers=extracted_answers,
            )
    elif payload.question_key == "preferred_study_days":
        if preferred_study_days:
            normalized_answer = ", ".join(preferred_study_days)
        else:
            return AgentIntakeAssistResponse(
                message="Aqui necesito los dias concretos. Puedes responder lunes a viernes o martes, jueves y sabado.",
                extracted_answers=extracted_answers,
            )
    elif payload.question_key == "learning_style":
        if learning_style:
            normalized_answer = learning_style
    elif payload.question_key == "age_range":
        if age_range:
            normalized_answer = age_range

    return AgentIntakeAssistResponse(
        message=f"Entiendo. Voy a tomar tu respuesta para {payload.question_title.lower()} como {normalized_answer}.",
        should_advance=True,
        normalized_answer=normalized_answer,
        extracted_answers=extracted_answers,
    )
