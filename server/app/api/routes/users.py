from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.onboarding import (
    OnboardingEvaluationRequest,
    OnboardingEvaluationResponse,
    OnboardingQuestionsResponse,
    SavedAssessmentResponse,
)
from app.models.profile import UpdateMyProfileRequest, UserProfileResponse
from app.services._shared import read_field
from app.services.onboarding_service import (
    evaluate_onboarding,
    get_latest_assessment,
    get_onboarding_questions,
)
from app.services.profile_service import ensure_profile_for_user, update_my_profile

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user=Depends(get_current_supabase_user)) -> UserProfileResponse:
    return ensure_profile_for_user(current_user)


@router.patch("/me", response_model=UserProfileResponse)
def patch_me(
    payload: UpdateMyProfileRequest,
    current_user=Depends(get_current_supabase_user),
) -> UserProfileResponse:
    profile = ensure_profile_for_user(current_user)
    return update_my_profile(read_field(profile, "id"), payload)


@router.get("/me/onboarding/questions", response_model=OnboardingQuestionsResponse)
def get_my_onboarding_questions(target_certification: str) -> OnboardingQuestionsResponse:
    return get_onboarding_questions(target_certification)


@router.post("/me/onboarding/evaluate", response_model=OnboardingEvaluationResponse)
def post_onboarding_evaluation(
    payload: OnboardingEvaluationRequest,
    current_user=Depends(get_current_supabase_user),
) -> OnboardingEvaluationResponse:
    return evaluate_onboarding(current_user, payload)


@router.get("/me/onboarding/latest", response_model=SavedAssessmentResponse | None)
def get_my_latest_assessment(
    current_user=Depends(get_current_supabase_user),
) -> SavedAssessmentResponse | None:
    return get_latest_assessment(current_user)
