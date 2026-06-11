from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    role: str = "employee"
    professional_role: str | None = None
    org_id: str | None = None
    team_id: str | None = None
    target_certification: str | None = None
    detected_level: str | None = None
    weekly_hours_available: int | None = None
    preferred_time: str | None = None
    preferred_start_hour: int | None = None
    preferred_study_days: list[str] = Field(default_factory=list)
    learning_style: list[str] = Field(default_factory=list)
    content_preferences: list[str] = Field(default_factory=list)
    study_techniques: list[str] = Field(default_factory=list)
    learning_goals: list[str] = Field(default_factory=list)
    technology_experience: list[str] = Field(default_factory=list)
    profile_version: int = 1
    onboarding_completed_at: str | None = None


class UpdateMyProfileRequest(BaseModel):
    full_name: str | None = None
    professional_role: str | None = None
    target_certification: str | None = None
    weekly_hours_available: int | None = None
    preferred_time: str | None = None
    preferred_start_hour: int | None = None
    preferred_study_days: list[str] | None = None
    learning_style: list[str] | None = None
    content_preferences: list[str] | None = None
    study_techniques: list[str] | None = None
    learning_goals: list[str] | None = None
    technology_experience: list[str] | None = None
    profile_version: int | None = None
    onboarding_completed_at: str | None = None
