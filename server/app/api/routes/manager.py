from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.course import CustomCourseRequest
from app.models.manager import (
    ManagerDashboardResponse,
    ManagerExportResponse,
    ManagerMemberDetailResponse,
    NudgeRequest,
    SupportMessageRequest,
    SupportMessageResponse,
    WeeklyTeamSummaryResponse,
)
from app.services.custom_course_service import create_custom_course, preview_custom_course
from app.services.manager_service import (
    export_team_report_pdf,
    get_member_detail,
    get_team_dashboard,
    get_weekly_team_summary,
    nudge_at_risk,
    send_member_nudge,
    send_support_message,
)
from app.services.ranking_service import get_team_ranking

router = APIRouter()


@router.get("/teams/{team_id}/ranking")
def get_ranking(team_id: str, current_user=Depends(get_current_supabase_user)) -> dict:
    """Ranking del equipo + record de tiempo + mejor metodologia (con agente)."""
    return get_team_ranking(current_user, team_id)


@router.post("/teams/{team_id}/members/{member_id}/nudge")
def post_member_nudge(
    team_id: str,
    member_id: str,
    payload: NudgeRequest,
    current_user=Depends(get_current_supabase_user),
) -> dict:
    """Empujon a un miembro (la IA lo redacta si no envias mensaje)."""
    return send_member_nudge(current_user, team_id, member_id, payload.message)


@router.post("/teams/{team_id}/nudge-at-risk")
def post_nudge_at_risk(team_id: str, current_user=Depends(get_current_supabase_user)) -> dict:
    """Avisa con IA a todos los miembros en riesgo de una vez."""
    return nudge_at_risk(current_user, team_id)


@router.post("/teams/{team_id}/custom-courses/preview")
def post_custom_course_preview(
    team_id: str,
    payload: CustomCourseRequest,
    current_user=Depends(get_current_supabase_user),
) -> dict:
    """Previsualiza el curso (estructura + si es certificable) SIN guardarlo."""
    return preview_custom_course(current_user, team_id, payload.markdown, payload.title)


@router.post("/teams/{team_id}/custom-courses")
def post_custom_course(
    team_id: str,
    payload: CustomCourseRequest,
    current_user=Depends(get_current_supabase_user),
) -> dict:
    """Crea el curso personalizado (scope del equipo) + embeddings para el RAG."""
    return create_custom_course(current_user, team_id, payload.markdown, payload.title)


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
