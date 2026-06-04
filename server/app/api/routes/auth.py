from fastapi import APIRouter

from app.models.auth import (
    AuthSessionResponse,
    EmailValidationRequest,
    EmailValidationResponse,
    LoginRequest,
    RegisterRequest,
)
from app.services.auth_service import analyze_email_address, register_mock_user, sign_in_mock_user

router = APIRouter()


@router.post("/validate-email", response_model=EmailValidationResponse)
def validate_email(payload: EmailValidationRequest) -> EmailValidationResponse:
    return analyze_email_address(payload.email)


@router.post("/register", response_model=AuthSessionResponse, status_code=201)
def register(payload: RegisterRequest) -> AuthSessionResponse:
    return register_mock_user(payload)


@router.post("/login", response_model=AuthSessionResponse)
def login(payload: LoginRequest) -> AuthSessionResponse:
    return sign_in_mock_user(payload)
