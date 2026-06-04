import logging
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.workiq_adapter import get_mock_calendar_context
from app.models.coach import ReminderGenerationResponse, ReminderResponse
from app.services._shared import response_data
from app.services.profile_service import ensure_profile_for_user

logger = logging.getLogger(__name__)


def _schedule_from_context(base: datetime, day_name: str, preferred_window: str) -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    target_idx = days.index(day_name)
    delta = (target_idx - base.weekday()) % 7
    hour, minute = [int(part) for part in preferred_window.split("-")[0].split(":")]
    candidate = (base + timedelta(days=delta)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate < base:
        candidate += timedelta(days=7)
    return candidate.isoformat()


def generate_my_reminders(auth_user: object) -> ReminderGenerationResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    plan_response = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    plans = response_data(plan_response, []) or []
    if not plans:
        return ReminderGenerationResponse(reminders=[], workiq_context={})

    plan = plans[0]
    workiq_context = plan.get("workiq_context") or get_mock_calendar_context(
        profile.preferred_time, profile.weekly_hours_available
    )
    deadline = datetime.fromisoformat(plan["deadline_at"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    days_remaining = max(0, (deadline - now).days)
    reminders = []
    preferred_days = workiq_context.get("recommended_study_days") or ["Monday", "Thursday"]
    preferred_windows = workiq_context.get("preferred_delivery_windows") or ["08:00-09:00"]
    avoid_days = set(workiq_context.get("avoid_days") or [])
    recent_reminders_response = (
        get_supabase_service_client()
        .table(settings.supabase_coach_reminders_table)
        .select("tone, status")
        .eq("user_id", profile.id)
        .order("created_at", desc=True)
        .limit(3)
        .execute()
    )
    recent_reminders = response_data(recent_reminders_response, []) or []
    ignored_recent = len([item for item in recent_reminders if item.get("status") == "dismissed"])
    adaptive_tone = "casual" if ignored_recent >= 2 else "concise" if ignored_recent == 1 else "formal"

    definitions = [
        (
            "standard",
            adaptive_tone,
            preferred_days[0],
            preferred_windows[0],
            "Tienes una sesion pendiente para mantener tu ritmo de certificacion sin presion innecesaria.",
        )
    ]
    for alert_offset in workiq_context.get("deadline_alert_offsets_days", [7, 3, 0]):
        if days_remaining >= alert_offset:
            target_day = preferred_days[min(len(preferred_days) - 1, len(definitions) % len(preferred_days))]
            while target_day in avoid_days:
                target_day = preferred_days[(preferred_days.index(target_day) + 1) % len(preferred_days)]
            definitions.append(
                (
                    "deadline",
                    "concise",
                    target_day,
                    preferred_windows[min(len(preferred_windows) - 1, len(definitions) % len(preferred_windows))],
                    (
                        "Hoy vence tu plan. Prioriza el ultimo hito pendiente."
                        if alert_offset == 0
                        else f"Tu plan vence en {alert_offset} dias. Reserva un bloque corto para avanzar hoy."
                    ),
                )
            )

    for kind, tone, day_name, window, message in definitions:
        scheduled_for = _schedule_from_context(now, day_name, window)
        response = (
            get_supabase_service_client()
            .table(settings.supabase_coach_reminders_table)
            .insert(
                {
                    "user_id": profile.id,
                    "plan_id": plan["id"],
                    "kind": kind,
                    "tone": tone,
                    "delivery_channel": "platform",
                    "message": message,
                    "scheduled_for": scheduled_for,
                    "status": "scheduled",
                }
            )
            .execute()
        )
        data = response_data(response, [])[0]
        reminders.append(ReminderResponse.model_validate(data))
    return ReminderGenerationResponse(reminders=reminders, workiq_context=workiq_context)


def list_my_reminders(auth_user: object) -> list[ReminderResponse]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    try:
        response = (
            get_supabase_service_client()
            .table(settings.supabase_coach_reminders_table)
            .select("*")
            .eq("user_id", profile.id)
            .order("scheduled_for")
            .execute()
        )
    except Exception as exc:
        logger.warning("Reminder lookup failed for user %s: %s", profile.id, exc)
        return []
    return [ReminderResponse.model_validate(item) for item in (response_data(response, []) or [])]
