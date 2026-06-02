from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    role: str = "employee"
    org_id: str | None = None
    team_id: str | None = None
    target_certification: str | None = None
    detected_level: str | None = None
    weekly_hours_available: int | None = None
    preferred_time: str | None = None
    learning_style: list[str] = Field(default_factory=list)
