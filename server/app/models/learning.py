from pydantic import BaseModel, Field

from app.models.certification import CertificationRouteResponse


class GenerateRouteRequest(BaseModel):
    target_certification: str


class GeneratePlanRequest(BaseModel):
    route_id: str
    weekly_hours: int | None = None
    preferred_time: str | None = None
    requested_deadline: str | None = None


class WeeklyMilestone(BaseModel):
    week: int
    title: str
    section_ids: list[str] = Field(default_factory=list)
    estimated_hours: int


class StudyPlanResponse(BaseModel):
    id: str | None = None
    route_id: str
    target_certification: str
    deadline_at: str
    weekly_hours: int
    weekly_milestones: list[WeeklyMilestone] = Field(default_factory=list)
    workiq_context: dict = Field(default_factory=dict)
    status: str = "active"


class TeamCertificationAssignmentRequest(BaseModel):
    target_certification: str
    member_ids: list[str] = Field(min_length=1)


class TeamCertificationAssignmentResponse(BaseModel):
    id: str | None = None
    team_id: str
    target_certification: str
    member_ids: list[str] = Field(default_factory=list)
    generated_plan_count: int = 0
    notifications_created: int = 0
    created_at: str | None = None


class RouteAndPlanBundle(BaseModel):
    route: CertificationRouteResponse
    plan: StudyPlanResponse
