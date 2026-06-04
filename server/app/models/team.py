from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class TeamMemberSummary(BaseModel):
    user_id: str
    full_name: str | None = None
    email: EmailStr
    role: Literal["manager", "employee"]
    certification: str | None = None
    team_id: str | None = None


class TeamInvitationSummary(BaseModel):
    id: str
    team_id: str
    org_id: str
    email: EmailStr
    role: Literal["manager", "employee"]
    status: Literal["pending", "accepted", "cancelled"]
    invited_by: str
    accepted_by: str | None = None
    invited_at: str | None = None
    responded_at: str | None = None


class TeamSummary(BaseModel):
    id: str
    name: str
    org_id: str
    manager_id: str
    organization_name: str | None = None
    member_count: int = 0
    pending_invites: int = 0


class CreateTeamRequest(BaseModel):
    team_name: str
    organization_name: str | None = None
    organization_id: str | None = None
    member_emails: list[EmailStr] = Field(default_factory=list)


class InviteTeamMembersRequest(BaseModel):
    emails: list[EmailStr] = Field(min_length=1)
    role: Literal["manager", "employee"] = "employee"


class UpdateMemberRoleRequest(BaseModel):
    role: Literal["manager", "employee"]


class AcceptInvitationResponse(BaseModel):
    message: str
    invitation: TeamInvitationSummary
    team: TeamSummary
