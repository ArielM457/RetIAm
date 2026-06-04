from pydantic import BaseModel, Field


class MemberRiskSummary(BaseModel):
    user_id: str
    full_name: str | None = None
    certification: str | None = None
    progress_percent: int
    days_to_deadline: int | None = None
    risk_status: str


class ManagerDashboardResponse(BaseModel):
    team_id: str
    team_name: str
    team_progress_percent: int
    members: list[MemberRiskSummary] = Field(default_factory=list)
    top_gaps: list[str] = Field(default_factory=list)


class WeeklyTeamSummaryResponse(BaseModel):
    team_id: str
    team_name: str
    summary_date: str
    delivery_channel: str
    highlights: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    upcoming_deadlines: list[MemberRiskSummary] = Field(default_factory=list)


class ManagerMemberDetailResponse(BaseModel):
    user_id: str
    full_name: str | None = None
    certification: str | None = None
    detected_level: str | None = None
    progress_percent: int
    days_to_deadline: int | None = None
    risk_status: str
    pending_sections: list[str] = Field(default_factory=list)


class SupportMessageRequest(BaseModel):
    message: str


class SupportMessageResponse(BaseModel):
    delivered: bool
    channel: str
    message: str


class ManagerExportResponse(BaseModel):
    team_id: str
    pdf_url: str
    generated_at: str
