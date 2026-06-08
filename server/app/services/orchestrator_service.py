"""Orquestador Gini Router (Fase 6).

Coordina el cierre de una leccion entre varios agentes para dar coherencia:
  1. Registra la leccion completada (progreso).
  2. Gini Insight: nota de ajuste segun el estilo de aprendizaje.
  3. Gini Coach: agenda el siguiente recordatorio adaptativo.
  4. Gini Router: decide y resume el proximo paso (continuar / examen).

Todo degrada con gracia: si Foundry esta apagado, usa mensajes plantilla; si
una escritura en Supabase falla, no rompe el flujo principal.
"""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import foundry_enabled, run_agent
from app.models.orchestration import CompleteLessonResponse
from app.services._shared import response_data
from app.services.course_service import get_course_detail, require_lesson_context
from app.services.profile_service import ensure_profile_for_user

logger = logging.getLogger(__name__)


def _client():
    return get_supabase_service_client()


def _get_owned_session(session_id: str, user_id: str) -> dict:
    settings = get_settings()
    rows = response_data(
        _client()
        .table(settings.supabase_learning_sessions_table)
        .select("*")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute(),
        [],
    ) or []
    if not rows:
        raise HTTPException(status_code=404, detail="Sesion no encontrada.")
    return rows[0]


def _course_lesson_ids(certification: str | None) -> list[str]:
    if not certification:
        return []
    course = get_course_detail(certification)
    if not course:
        return []
    return [lesson.id for section in course.sections for lesson in section.lessons if lesson.id]


def _insight_note(learning_style: list[str] | None) -> str:
    if not learning_style:
        return "Seguimos ajustando tu experiencia segun como aprendes mejor."
    pretty = ", ".join(learning_style)
    return f"Estamos priorizando contenido en tu estilo preferido ({pretty}) para las proximas lecciones."


def _schedule_next_reminder(user_id: str, plan_id: str | None, certification: str | None) -> tuple[str | None, str | None]:
    settings = get_settings()
    scheduled_for = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
    message = (
        f"Buen avance en {certification or 'tu certificacion'}. Reserva un bloque manana "
        "para tu siguiente leccion y mantener el ritmo."
    )
    agent = run_agent(
        "gini-coach",
        f"Escribe un recordatorio breve y motivador (max 30 palabras) para retomar la siguiente "
        f"leccion de {certification or 'la certificacion'} manana.",
        temperature=0.6,
        max_tokens=120,
        ground=False,
    )
    if agent:
        message = agent["text"]
    try:
        _client().table(settings.supabase_coach_reminders_table).insert(
            {
                "user_id": user_id,
                "plan_id": plan_id,
                "kind": "standard",
                "tone": "casual",
                "delivery_channel": "platform",
                "message": message,
                "scheduled_for": scheduled_for,
                "status": "scheduled",
            }
        ).execute()
    except Exception as exc:
        logger.warning("No se pudo agendar recordatorio de coach: %s", exc)
        return message, None
    return message, scheduled_for


def complete_lesson(auth_user: object, session_id: str, lesson_id: str) -> CompleteLessonResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    context = require_lesson_context(lesson_id)
    certification = context.get("certification_code")
    session = _get_owned_session(session_id, profile.id)
    plan_id = session.get("plan_id")

    # 1. Registrar leccion completada (idempotente por user+lesson).
    try:
        _client().table(settings.supabase_lesson_completions_table).upsert(
            {
                "user_id": profile.id,
                "plan_id": plan_id,
                "lesson_id": lesson_id,
                "session_id": session_id,
                "status": "completed",
            },
            on_conflict="user_id,lesson_id",
        ).execute()
    except Exception as exc:
        logger.warning("No se pudo registrar lesson_completion: %s", exc)

    # 2. Progreso del curso.
    lesson_ids = _course_lesson_ids(certification)
    total_lessons = len(lesson_ids)
    completed_lessons = 0
    if lesson_ids:
        completed_rows = response_data(
            _client()
            .table(settings.supabase_lesson_completions_table)
            .select("lesson_id")
            .eq("user_id", profile.id)
            .eq("status", "completed")
            .in_("lesson_id", lesson_ids)
            .execute(),
            [],
        ) or []
        completed_lessons = len({row["lesson_id"] for row in completed_rows})
    progress_percent = int((completed_lessons / total_lessons) * 100) if total_lessons else 0

    # 3. Gini Insight (nota de estilo).
    insight_note = _insight_note(getattr(profile, "learning_style", None))

    # 4. Gini Coach (siguiente recordatorio).
    coach_message, coach_scheduled_for = _schedule_next_reminder(profile.id, plan_id, certification)

    # 5. Gini Router (proximo paso).
    if total_lessons and completed_lessons >= total_lessons:
        next_action = "final_exam"
        next_action_label = "Completaste todas las lecciones. Ya puedes rendir el examen final."
    else:
        next_action = "continue"
        next_action_label = "Continua con la siguiente leccion de tu plan."
    source_mode = "foundry" if foundry_enabled() else "mock"

    return CompleteLessonResponse(
        lesson_id=lesson_id,
        status="completed",
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        progress_percent=progress_percent,
        insight_note=insight_note,
        coach_message=coach_message,
        coach_scheduled_for=coach_scheduled_for,
        next_action=next_action,
        next_action_label=next_action_label,
        source_mode=source_mode,
    )
