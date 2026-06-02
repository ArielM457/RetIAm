from fastapi import APIRouter

from app.models.auth import EmailValidationRequest, EmailValidationResponse
from app.services.auth_service import validate_corporate_email

router = APIRouter()


@router.post("/validate-email", response_model=EmailValidationResponse)
def validate_email(payload: EmailValidationRequest) -> EmailValidationResponse:
    valid = validate_corporate_email(payload.email)
    return EmailValidationResponse(
        email=payload.email,
        is_valid=valid,
        message=(
            "Correo corporativo valido para la demo."
            if valid
            else "Usa un correo corporativo. Los dominios publicos estan bloqueados."
        ),
    )
