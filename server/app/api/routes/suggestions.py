from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.suggestion import SuggestionRequest, SuggestionResponse, TeamSuggestionSummary
from app.services.suggestion_service import create_suggestion, get_team_suggestion_summary, list_my_suggestions

router = APIRouter()


@router.post("", response_model=SuggestionResponse, status_code=201)
def post_suggestion(
    payload: SuggestionRequest,
    current_user=Depends(get_current_supabase_user),
) -> SuggestionResponse:
    return create_suggestion(current_user, payload)


@router.get("/mine", response_model=list[SuggestionResponse])
def get_my_suggestions(current_user=Depends(get_current_supabase_user)) -> list[SuggestionResponse]:
    return list_my_suggestions(current_user)


@router.get("/team/{team_id}/summary", response_model=TeamSuggestionSummary)
def get_team_summary(
    team_id: str,
    current_user=Depends(get_current_supabase_user),
) -> TeamSuggestionSummary:
    return get_team_suggestion_summary(current_user, team_id)
