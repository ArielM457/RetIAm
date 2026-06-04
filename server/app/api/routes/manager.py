from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.manager import (
    ManagerDashboardResponse,
    ManagerExportResponse,
    ManagerMemberDetailResponse,
    SupportMessageRequest,
    SupportMessageResponse,
    WeeklyTeamSummaryResponse,
)
from app.services.manager_service import (
    export_team_report_pdf,
    get_member_detail,
    get_team_dashboard,
    get_weekly_team_summary,
    send_support_message,
)

router = APIRouter()


@router.get("/teams/{team_id}/dashboard", response_model=ManagerDashboardResponse)
def get_dashboard(team_id: str, current_user=Depends(get_current_supabase_user)) -> ManagerDashboardResponse:
    return get_team_dashboard(current_user, team_id)


@router.get("/teams/{team_id}/weekly-summary", response_model=WeeklyTeamSummaryResponse)
def get_weekly_summary(
    team_id: str,
    current_user=Depends(get_current_supabase_user),
) -> WeeklyTeamSummaryResponse:
    return get_weekly_team_summary(current_user, team_id)


@router.get("/teams/{team_id}/export-pdf", response_model=ManagerExportResponse)
def get_export_pdf(
    team_id: str,
    current_user=Depends(get_current_supabase_user),
) -> ManagerExportResponse:
    return export_team_report_pdf(current_user, team_id)


@router.get(
    "/teams/{team_id}/members/{member_id}",
    response_model=ManagerMemberDetailResponse,
)
def get_member(
    team_id: str,
    member_id: str,
    current_user=Depends(get_current_supabase_user),
) -> ManagerMemberDetailResponse:
    return get_member_detail(current_user, team_id, member_id)


@router.post(
    "/teams/{team_id}/members/{member_id}/support-message",
    response_model=SupportMessageResponse,
)
def post_support_message(
    team_id: str,
    member_id: str,
    payload: SupportMessageRequest,
    current_user=Depends(get_current_supabase_user),
) -> SupportMessageResponse:
    return send_support_message(current_user, team_id, member_id, payload)
