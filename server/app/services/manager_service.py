from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.manager import (
    ManagerDashboardResponse,
    ManagerExportResponse,
    ManagerMemberDetailResponse,
    MemberRiskSummary,
    SupportMessageRequest,
    SupportMessageResponse,
    WeeklyTeamSummaryResponse,
)
from app.services._shared import response_data
from app.services.pdf_service import generate_simple_pdf
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import _ensure_manager_access, _get_team_record


def _member_progress(member_id: str) -> tuple[int, list[str], str | None]:
    settings = get_settings()
    plans = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .select("*")
        .eq("user_id", member_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    plan_data = (response_data(plans, []) or [None])[0]
    if not plan_data:
        return 0, [], None
    milestones = plan_data.get("weekly_milestones") or []
    total_sections = sum(len(item.get("section_ids", [])) for item in milestones) or 1
    sessions = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .select("*")
        .eq("user_id", member_id)
        .eq("plan_id", plan_data["id"])
        .execute()
    )
    completed = len([item for item in (response_data(sessions, []) or []) if item.get("status") == "completed"])
    progress = int((completed / total_sections) * 100)
    pending = []
    for milestone in milestones:
        for section_id in milestone.get("section_ids", []):
            if completed < total_sections:
                pending.append(section_id)
    return progress, pending, plan_data["deadline_at"]


def _risk_status(progress_percent: int, deadline_at: str | None) -> tuple[str, int | None]:
    if not deadline_at:
        return "yellow", None
    deadline = datetime.fromisoformat(deadline_at.replace("Z", "+00:00"))
    days = max(0, (deadline - datetime.now(timezone.utc)).days)
    if days <= 3 and progress_percent < 70:
        return "red", days
    if days <= 7 and progress_percent < 80:
        return "yellow", days
    return "green", days


def _compute_top_gaps(member_ids: list[str]) -> list[str]:
    settings = get_settings()
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    sessions_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .select("section_title,evaluation,started_at,user_id")
        .in_("user_id", member_ids or [""])
        .gte("started_at", since)
        .execute()
    )
    exams_response = (
        get_supabase_service_client()
        .table(settings.supabase_exam_attempts_table)
        .select("failed_sections,submitted_at,user_id")
        .in_("user_id", member_ids or [""])
        .gte("submitted_at", since)
        .execute()
    )
    gap_counts: dict[str, int] = {}
    for item in response_data(sessions_response, []) or []:
        evaluation = item.get("evaluation") or {}
        quiz = evaluation.get("quiz") or {}
        lab = evaluation.get("lab") or {}
        if quiz and not quiz.get("passed", True):
            gap_counts[item["section_title"]] = gap_counts.get(item["section_title"], 0) + 1
        if lab and not lab.get("passed", True):
            gap_counts[item["section_title"]] = gap_counts.get(item["section_title"], 0) + 1
    for attempt in response_data(exams_response, []) or []:
        for section in attempt.get("failed_sections") or []:
            gap_counts[section] = gap_counts.get(section, 0) + 1
    ordered = sorted(gap_counts.items(), key=lambda item: item[1], reverse=True)
    return [name for name, _ in ordered[:3]]


def get_team_dashboard(auth_user: object, team_id: str) -> ManagerDashboardResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    team = _ensure_manager_access(team_id, profile.id)
    members_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("user_id")
        .eq("team_id", team_id)
        .execute()
    )
    members = response_data(members_response, []) or []
    summaries: list[MemberRiskSummary] = []
    progress_values: list[int] = []
    member_ids = [member["user_id"] for member in members]
    for member in members:
        member_profile_response = (
            get_supabase_service_client()
            .table(settings.supabase_profiles_table)
            .select("*")
            .eq("id", member["user_id"])
            .limit(1)
            .execute()
        )
        member_profile = (response_data(member_profile_response, []) or [None])[0]
        if not member_profile:
            continue
        progress, _, deadline = _member_progress(member["user_id"])
        risk, days = _risk_status(progress, deadline)
        progress_values.append(progress)
        summaries.append(
            MemberRiskSummary(
                user_id=member_profile["id"],
                full_name=member_profile.get("full_name"),
                certification=member_profile.get("target_certification"),
                progress_percent=progress,
                days_to_deadline=days,
                risk_status=risk,
            )
        )
    average = int(sum(progress_values) / len(progress_values)) if progress_values else 0
    return ManagerDashboardResponse(
        team_id=team_id,
        team_name=team["name"],
        team_progress_percent=average,
        members=summaries,
        top_gaps=_compute_top_gaps(member_ids),
    )


def get_member_detail(auth_user: object, team_id: str, member_id: str) -> ManagerMemberDetailResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)
    profile_response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .select("*")
        .eq("id", member_id)
        .limit(1)
        .execute()
    )
    member = (response_data(profile_response, []) or [None])[0]
    if not member:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")
    progress, pending_sections, deadline = _member_progress(member_id)
    risk, days = _risk_status(progress, deadline)
    return ManagerMemberDetailResponse(
        user_id=member["id"],
        full_name=member.get("full_name"),
        certification=member.get("target_certification"),
        detected_level=member.get("detected_level"),
        progress_percent=progress,
        days_to_deadline=days,
        risk_status=risk,
        pending_sections=pending_sections[:6],
    )


def send_support_message(
    auth_user: object,
    team_id: str,
    member_id: str,
    payload: SupportMessageRequest,
) -> SupportMessageResponse:
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)
    return SupportMessageResponse(
        delivered=True,
        channel="platform",
        message=payload.message,
    )


def get_weekly_team_summary(auth_user: object, team_id: str) -> WeeklyTeamSummaryResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    team = _ensure_manager_access(team_id, profile.id)
    members_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("user_id")
        .eq("team_id", team_id)
        .execute()
    )
    members = response_data(members_response, []) or []
    member_ids = [member["user_id"] for member in members]
    dashboard = get_team_dashboard(auth_user, team_id)
    since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    sessions_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_sessions_table)
        .select("status,user_id,completed_at")
        .in_("user_id", member_ids or [""])
        .gte("started_at", since)
        .execute()
    )
    completed_last_week = len(
        [item for item in (response_data(sessions_response, []) or []) if item.get("status") == "completed"]
    )
    risks = [member for member in dashboard.members if member.risk_status in {"yellow", "red"}]
    upcoming_deadlines = [member for member in dashboard.members if (member.days_to_deadline or 999) <= 7]
    highlights = [
        f"Se completaron {completed_last_week} sesiones en los ultimos 7 dias.",
        f"El avance promedio del equipo esta en {dashboard.team_progress_percent} por ciento.",
        (
            "No detectamos brechas criticas esta semana."
            if not dashboard.top_gaps
            else f"Las mayores brechas del equipo son: {', '.join(dashboard.top_gaps)}."
        ),
    ]
    risk_lines = [
        f"{member.full_name or member.user_id} esta en riesgo {member.risk_status} con {member.progress_percent} por ciento de avance."
        for member in risks
    ]
    return WeeklyTeamSummaryResponse(
        team_id=team_id,
        team_name=team["name"],
        summary_date=datetime.now(timezone.utc).date().isoformat(),
        delivery_channel="teams",
        highlights=highlights,
        risks=risk_lines,
        upcoming_deadlines=upcoming_deadlines,
    )


def export_team_report_pdf(auth_user: object, team_id: str) -> ManagerExportResponse:
    team_summary = get_weekly_team_summary(auth_user, team_id)
    output_path = Path(__file__).resolve().parents[2] / "generated" / "reports" / f"{team_id}.pdf"
    lines = team_summary.highlights + team_summary.risks
    if team_summary.upcoming_deadlines:
        lines.extend(
            [
                f"Proximo vencimiento: {member.full_name or member.user_id} en {member.days_to_deadline} dias."
                for member in team_summary.upcoming_deadlines
            ]
        )
    generate_simple_pdf(output_path, f"Reporte semanal de {team_summary.team_name}", lines)
    generated_at = datetime.now(timezone.utc).isoformat()
    return ManagerExportResponse(
        team_id=team_id,
        pdf_url=f"/generated/reports/{team_id}.pdf",
        generated_at=generated_at,
    )
