from pydantic import BaseModel, Field

from app.models.certification import CertificationRouteResponse


class GenerateRouteRequest(BaseModel):
    target_certification: str


class EnrollCourseRequest(BaseModel):
    certification_code: str
    confirm: bool = True


class GeneratePlanRequest(BaseModel):
    route_id: str
    weekly_hours: int | None = None
    preferred_time: str | None = None
    requested_deadline: str | None = None


class StudySessionPlan(BaseModel):
    session_id: str
    title: str
    session_type: str
    day_name: str
    time_window: str
    duration_minutes: int
    section_id: str
    lesson_ids: list[str] = Field(default_factory=list)
    methodologies: list[str] = Field(default_factory=list)
    focus_points: list[str] = Field(default_factory=list)
    is_review: bool = False
    unlocks: list[str] = Field(default_factory=list)


class AgendaItemResponse(BaseModel):
    id: str | None = None
    enrollment_id: str | None = None
    plan_id: str | None = None
    route_id: str | None = None
    title: str
    item_type: str
    related_session_id: str | None = None
    related_section_id: str | None = None
    related_lesson_ids: list[str] = Field(default_factory=list)
    scheduled_start: str
    scheduled_end: str
    time_window: str | None = None
    status: str = "scheduled"
    metadata: dict = Field(default_factory=dict)


class PlanCheckin(BaseModel):
    kind: str
    title: str
    trigger: str
    success_criteria: list[str] = Field(default_factory=list)
    recovery_action: str | None = None


class WeeklyMilestone(BaseModel):
    week: int
    title: str
    section_ids: list[str] = Field(default_factory=list)
    estimated_hours: int
    focus: str | None = None
    methodology_notes: list[str] = Field(default_factory=list)
    sessions: list[StudySessionPlan] = Field(default_factory=list)
    checkins: list[PlanCheckin] = Field(default_factory=list)


class StudyPlanResponse(BaseModel):
    id: str | None = None
    route_id: str
    target_certification: str
    deadline_at: str
    weekly_hours: int
    weekly_milestones: list[WeeklyMilestone] = Field(default_factory=list)
    workiq_context: dict = Field(default_factory=dict)
    status: str = "active"
    personalization_summary: list[str] = Field(default_factory=list)


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


class CourseEnrollmentResponse(BaseModel):
    id: str | None = None
    user_id: str
    course_id: str
    certification_code: str
    status: str = "enrolled"
    enrolled_at: str | None = None
    activated_route_id: str | None = None
    activated_plan_id: str | None = None
    preferences_snapshot: dict = Field(default_factory=dict)
    personalization_summary: list[str] = Field(default_factory=list)
    current_section_id: str | None = None
    current_session_id: str | None = None


class EnrollmentFlowResponse(BaseModel):
    enrollment: CourseEnrollmentResponse
    route: CertificationRouteResponse
    plan: StudyPlanResponse
    agenda: list[AgendaItemResponse] = Field(default_factory=list)
