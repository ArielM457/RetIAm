from typing import Literal

from pydantic import BaseModel, EmailStr


class EmailValidationRequest(BaseModel):
    email: EmailStr


class EmailValidationResponse(BaseModel):
    email: EmailStr
    is_valid: bool
    is_corporate_domain: bool
    should_recommend_custom_domain: bool
    recommendation: str | None = None
    message: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: Literal["manager", "employee"] = "employee"
    team_access_code: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthenticatedUserSummary(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    role: Literal["manager", "employee"] = "employee"
    org_id: str | None = None
    team_id: str | None = None


class AuthSessionResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: int | None = None
    user: AuthenticatedUserSummary
    message: str
