from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.coach import ReminderGenerationResponse, ReminderResponse
from app.services.coach_service import generate_my_reminders, list_my_reminders

router = APIRouter()


@router.post("/reminders/generate", response_model=ReminderGenerationResponse)
def post_generate_reminders(current_user=Depends(get_current_supabase_user)) -> ReminderGenerationResponse:
    return generate_my_reminders(current_user)


@router.get("/reminders/mine", response_model=list[ReminderResponse])
def get_my_reminders(current_user=Depends(get_current_supabase_user)) -> list[ReminderResponse]:
    return list_my_reminders(current_user)
