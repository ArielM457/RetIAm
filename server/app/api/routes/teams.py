from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.team import (
    AcceptInvitationResponse,
    CreateTeamRequest,
    InviteTeamMembersRequest,
    TeamInvitationSummary,
    TeamMemberSummary,
    TeamSummary,
    UpdateMemberRoleRequest,
)
from app.services.team_service import (
    accept_invitation,
    create_team,
    invite_team_members,
    list_my_invitations,
    list_my_teams,
    list_team_members,
    update_member_role,
)

router = APIRouter()


@router.get("", response_model=list[TeamSummary])
def get_my_teams(current_user=Depends(get_current_supabase_user)) -> list[TeamSummary]:
    return list_my_teams(current_user)


@router.post("", response_model=TeamSummary, status_code=201)
def post_team(
    payload: CreateTeamRequest,
    current_user=Depends(get_current_supabase_user),
) -> TeamSummary:
    return create_team(current_user, payload)


@router.get("/{team_id}/members", response_model=list[TeamMemberSummary])
def get_team_members(team_id: str, current_user=Depends(get_current_supabase_user)) -> list[TeamMemberSummary]:
    return list_team_members(current_user, team_id)


@router.post("/{team_id}/invites", response_model=list[TeamInvitationSummary], status_code=201)
def post_team_invites(
    team_id: str,
    payload: InviteTeamMembersRequest,
    current_user=Depends(get_current_supabase_user),
) -> list[TeamInvitationSummary]:
    return invite_team_members(current_user, team_id, payload)


@router.get("/invitations/mine", response_model=list[TeamInvitationSummary])
def get_my_invitations(current_user=Depends(get_current_supabase_user)) -> list[TeamInvitationSummary]:
    return list_my_invitations(current_user)


@router.post("/invitations/{invitation_id}/accept", response_model=AcceptInvitationResponse)
def post_accept_invitation(
    invitation_id: str,
    current_user=Depends(get_current_supabase_user),
) -> AcceptInvitationResponse:
    return accept_invitation(current_user, invitation_id)


@router.patch("/{team_id}/members/{member_id}/role", response_model=TeamMemberSummary)
def patch_member_role(
    team_id: str,
    member_id: str,
    payload: UpdateMemberRoleRequest,
    current_user=Depends(get_current_supabase_user),
) -> TeamMemberSummary:
    return update_member_role(current_user, team_id, member_id, payload)
