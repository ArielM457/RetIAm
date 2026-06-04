from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.certification import CertificationRouteResponse
from app.models.learning import (
    GeneratePlanRequest,
    GenerateRouteRequest,
    StudyPlanResponse,
    TeamCertificationAssignmentRequest,
    TeamCertificationAssignmentResponse,
)
from app.services.learning_service import (
    assign_certification_to_team,
    generate_learning_route,
    generate_study_plan,
    get_my_latest_plan,
    get_my_latest_route,
)

router = APIRouter()


@router.post("/routes", response_model=CertificationRouteResponse, status_code=201)
def post_route(
    payload: GenerateRouteRequest,
    current_user=Depends(get_current_supabase_user),
) -> CertificationRouteResponse:
    return generate_learning_route(current_user, payload)


@router.get("/routes/latest", response_model=CertificationRouteResponse | None)
def get_latest_route(current_user=Depends(get_current_supabase_user)) -> CertificationRouteResponse | None:
    return get_my_latest_route(current_user)


@router.post("/plans", response_model=StudyPlanResponse, status_code=201)
def post_plan(
    payload: GeneratePlanRequest,
    current_user=Depends(get_current_supabase_user),
) -> StudyPlanResponse:
    return generate_study_plan(current_user, payload)


@router.get("/plans/latest", response_model=StudyPlanResponse | None)
def get_latest_plan(current_user=Depends(get_current_supabase_user)) -> StudyPlanResponse | None:
    return get_my_latest_plan(current_user)


@router.post(
    "/teams/{team_id}/assignments",
    response_model=TeamCertificationAssignmentResponse,
    status_code=201,
)
def post_team_assignment(
    team_id: str,
    payload: TeamCertificationAssignmentRequest,
    current_user=Depends(get_current_supabase_user),
) -> TeamCertificationAssignmentResponse:
    return assign_certification_to_team(current_user, team_id, payload)
