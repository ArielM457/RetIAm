from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.profile import UserProfileResponse
from app.services.profile_service import ensure_profile_for_user

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user=Depends(get_current_supabase_user)) -> UserProfileResponse:
    return ensure_profile_for_user(current_user)
