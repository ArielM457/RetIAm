from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.team import (
    AcceptInvitationResponse,
    CreateTeamRequest,
    InviteTeamMembersRequest,
    TeamInvitationSummary,
    TeamMemberSummary,
    TeamSummary,
    UpdateMemberRoleRequest,
)
from app.services._shared import response_data
from app.services.auth_service import analyze_email_address, normalize_email
from app.services.profile_service import ensure_profile_for_user


def _get_profile_record(user_id: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado.")
    return data[0]


def _get_team_record(team_id: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_teams_table)
        .select("*")
        .eq("id", team_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado.")
    return data[0]


def _get_org_name(org_id: str) -> str | None:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_organizations_table)
        .select("name")
        .eq("id", org_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    return data[0]["name"] if data else None


def _build_team_summary(team: dict) -> TeamSummary:
    settings = get_settings()
    members_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("user_id", count="exact")
        .eq("team_id", team["id"])
        .execute()
    )
    invites_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_invitations_table)
        .select("id", count="exact")
        .eq("team_id", team["id"])
        .eq("status", "pending")
        .execute()
    )
    member_count = getattr(members_response, "count", None) or len(response_data(members_response, []))
    pending_invites = getattr(invites_response, "count", None) or len(response_data(invites_response, []))
    return TeamSummary(
        id=team["id"],
        name=team["name"],
        org_id=team["org_id"],
        manager_id=team["manager_id"],
        organization_name=_get_org_name(team["org_id"]),
        member_count=member_count,
        pending_invites=pending_invites,
    )


def _ensure_manager_access(team_id: str, user_id: str) -> dict:
    team = _get_team_record(team_id)
    if team["manager_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el manager del equipo puede realizar esta accion.",
        )
    return team


def _create_organization_if_needed(payload: CreateTeamRequest, current_profile: dict) -> str:
    settings = get_settings()
    if payload.organization_id:
        return payload.organization_id
    if current_profile.get("org_id"):
        return current_profile["org_id"]
    if not payload.organization_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Necesitamos un nombre de organizacion para crear el primer equipo.",
        )

    response = (
        get_supabase_service_client()
        .table(settings.supabase_organizations_table)
        .insert({"name": payload.organization_name})
        .execute()
    )
    data = response_data(response, [])
    return data[0]["id"]


def create_team(auth_user: object, payload: CreateTeamRequest) -> TeamSummary:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    current_profile = _get_profile_record(profile.id)
    org_id = _create_organization_if_needed(payload, current_profile)

    response = (
        get_supabase_service_client()
        .table(settings.supabase_teams_table)
        .insert(
            {
                "name": payload.team_name,
                "org_id": org_id,
                "manager_id": profile.id,
            }
        )
        .execute()
    )
    team_data = response_data(response, [])[0]

    get_supabase_service_client().table(settings.supabase_profiles_table).update(
        {
            "role": "manager",
            "org_id": org_id,
        }
    ).eq("id", profile.id).execute()

    get_supabase_service_client().table(settings.supabase_team_members_table).upsert(
        {
            "team_id": team_data["id"],
            "user_id": profile.id,
        }
    ).execute()

    if payload.member_emails:
        invite_team_members(auth_user, team_data["id"], InviteTeamMembersRequest(emails=payload.member_emails))

    return _build_team_summary(team_data)


def list_my_teams(auth_user: object) -> list[TeamSummary]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    manager_response = (
        get_supabase_service_client()
        .table(settings.supabase_teams_table)
        .select("*")
        .eq("manager_id", profile.id)
        .execute()
    )
    manager_teams = response_data(manager_response, []) or []

    memberships_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("team_id")
        .eq("user_id", profile.id)
        .execute()
    )
    membership_ids = {item["team_id"] for item in (response_data(memberships_response, []) or [])}
    manager_ids = {team["id"] for team in manager_teams}
    all_ids = membership_ids | manager_ids

    teams: list[dict] = manager_teams[:]
    for team_id in all_ids - manager_ids:
        teams.append(_get_team_record(team_id))

    seen: set[str] = set()
    unique_teams = []
    for team in teams:
        if team["id"] in seen:
            continue
        seen.add(team["id"])
        unique_teams.append(_build_team_summary(team))
    return unique_teams


def list_team_members(auth_user: object, team_id: str) -> list[TeamMemberSummary]:
    profile = ensure_profile_for_user(auth_user)
    team = _get_team_record(team_id)
    if team["manager_id"] != profile.id and profile.team_id != team_id:
        membership_response = (
            get_supabase_service_client()
            .table(get_settings().supabase_team_members_table)
            .select("team_id")
            .eq("team_id", team_id)
            .eq("user_id", profile.id)
            .limit(1)
            .execute()
        )
        if not response_data(membership_response, []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este equipo.",
            )

    settings = get_settings()
    memberships = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("user_id")
        .eq("team_id", team_id)
        .execute()
    )
    members = response_data(memberships, []) or []
    summaries: list[TeamMemberSummary] = []
    for member in members:
        record = _get_profile_record(member["user_id"])
        summaries.append(
            TeamMemberSummary(
                user_id=record["id"],
                full_name=record.get("full_name"),
                email=record["email"],
                role=record["role"],
                certification=record.get("target_certification"),
                team_id=record.get("team_id"),
            )
        )
    return summaries


def invite_team_members(
    auth_user: object,
    team_id: str,
    payload: InviteTeamMembersRequest,
) -> list[TeamInvitationSummary]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    team = _ensure_manager_access(team_id, profile.id)

    invitations: list[TeamInvitationSummary] = []
    for email in payload.emails:
        assessment = analyze_email_address(email)
        if not assessment.is_valid:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=assessment.message)

        normalized_email = normalize_email(email)
        existing_profile_response = (
            get_supabase_service_client()
            .table(settings.supabase_profiles_table)
            .select("id, team_id, role")
            .eq("email", normalized_email)
            .limit(1)
            .execute()
        )
        existing_profile = (response_data(existing_profile_response, []) or [None])[0]
        if existing_profile and existing_profile.get("team_id") and existing_profile["team_id"] != team_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{normalized_email} ya pertenece a otro equipo.",
            )

        invitation_response = (
            get_supabase_service_client()
            .table(settings.supabase_team_invitations_table)
            .upsert(
                {
                    "team_id": team_id,
                    "org_id": team["org_id"],
                    "email": normalized_email,
                    "role": payload.role,
                    "status": "pending",
                    "invited_by": profile.id,
                },
                on_conflict="team_id,email",
            )
            .execute()
        )
        invitation_data = response_data(invitation_response, [])[0]
        invitations.append(TeamInvitationSummary.model_validate(invitation_data))

    return invitations


def list_my_invitations(auth_user: object) -> list[TeamInvitationSummary]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_team_invitations_table)
        .select("*")
        .eq("email", normalize_email(profile.email))
        .eq("status", "pending")
        .execute()
    )
    return [TeamInvitationSummary.model_validate(item) for item in (response_data(response, []) or [])]


def accept_invitation(auth_user: object, invitation_id: str) -> AcceptInvitationResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    current_profile = _get_profile_record(profile.id)

    invitation_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_invitations_table)
        .select("*")
        .eq("id", invitation_id)
        .eq("status", "pending")
        .limit(1)
        .execute()
    )
    invitation_data = (response_data(invitation_response, []) or [None])[0]
    if not invitation_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitacion no encontrada.")

    if normalize_email(profile.email) != normalize_email(invitation_data["email"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta invitacion no corresponde al correo autenticado.",
        )

    if current_profile.get("team_id") and current_profile["team_id"] != invitation_data["team_id"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este usuario ya pertenece a otro equipo.",
        )

    responded_at = datetime.now(timezone.utc).isoformat()
    get_supabase_service_client().table(settings.supabase_profiles_table).update(
        {
            "org_id": invitation_data["org_id"],
            "team_id": invitation_data["team_id"],
            "role": invitation_data["role"],
        }
    ).eq("id", profile.id).execute()

    get_supabase_service_client().table(settings.supabase_team_members_table).upsert(
        {
            "team_id": invitation_data["team_id"],
            "user_id": profile.id,
        }
    ).execute()

    updated_invitation_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_invitations_table)
        .update(
            {
                "status": "accepted",
                "accepted_by": profile.id,
                "responded_at": responded_at,
            }
        )
        .eq("id", invitation_id)
        .execute()
    )
    updated_invitation = response_data(updated_invitation_response, [])[0]
    team = _build_team_summary(_get_team_record(invitation_data["team_id"]))
    return AcceptInvitationResponse(
        message="Invitacion aceptada correctamente.",
        invitation=TeamInvitationSummary.model_validate(updated_invitation),
        team=team,
    )


def update_member_role(
    auth_user: object,
    team_id: str,
    member_id: str,
    payload: UpdateMemberRoleRequest,
) -> TeamMemberSummary:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)

    membership_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("*")
        .eq("team_id", team_id)
        .eq("user_id", member_id)
        .limit(1)
        .execute()
    )
    if not response_data(membership_response, []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Miembro no encontrado en el equipo.")

    profile_response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .update({"role": payload.role})
        .eq("id", member_id)
        .execute()
    )
    updated = response_data(profile_response, [])[0]
    return TeamMemberSummary(
        user_id=updated["id"],
        full_name=updated.get("full_name"),
        email=updated["email"],
        role=updated["role"],
        certification=updated.get("target_certification"),
        team_id=updated.get("team_id"),
    )
