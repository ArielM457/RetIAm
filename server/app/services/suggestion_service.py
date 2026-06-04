from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.suggestion import SuggestionRequest, SuggestionResponse, TeamSuggestionSummary
from app.services._shared import response_data
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import _ensure_manager_access


def _evaluate_suggestion(message: str) -> tuple[str, str]:
    lowered = message.lower()
    if len(lowered.split()) < 5:
        return (
            "needs_context",
            "Entendemos tu idea, pero necesitamos un poco mas de detalle. Podrias contarnos un ejemplo concreto?",
        )
    if any(keyword in lowered for keyword in ["pdf", "offline", "dashboard", "recordatorio", "contenido"]):
        return (
            "applicable",
            "Gracias por tu sugerencia. La agregamos al backlog con prioridad alta.",
        )
    return (
        "queued",
        "Tu sugerencia es valida y la tenemos en cuenta. La agregamos a nuestra lista de mejoras futuras.",
    )


def create_suggestion(auth_user: object, payload: SuggestionRequest) -> SuggestionResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    status_value, agent_response = _evaluate_suggestion(payload.message)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_suggestions_table)
        .insert(
            {
                "user_id": profile.id,
                "team_id": profile.team_id,
                "category": payload.category,
                "message": payload.message,
                "status": status_value,
                "agent_response": agent_response,
                "reviewed_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .execute()
    )
    data = response_data(response, [])[0]
    return SuggestionResponse.model_validate(data)


def list_my_suggestions(auth_user: object) -> list[SuggestionResponse]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_suggestions_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("created_at", desc=True)
        .execute()
    )
    return [SuggestionResponse.model_validate(item) for item in (response_data(response, []) or [])]


def get_team_suggestion_summary(auth_user: object, team_id: str) -> TeamSuggestionSummary:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_suggestions_table)
        .select("*")
        .eq("team_id", team_id)
        .execute()
    )
    suggestions = response_data(response, []) or []
    by_category: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for item in suggestions:
        by_category[item["category"]] = by_category.get(item["category"], 0) + 1
        by_status[item["status"]] = by_status.get(item["status"], 0) + 1
    return TeamSuggestionSummary(team_id=team_id, totals_by_category=by_category, totals_by_status=by_status)
