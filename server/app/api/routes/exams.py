from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.exam import (
    CertificateResponse,
    CertificateVerificationResponse,
    FinalExamAttemptResponse,
    StartFinalExamRequest,
    SubmitFinalExamRequest,
)
from app.services.exam_service import (
    list_my_certificates,
    start_final_exam,
    submit_final_exam,
    verify_certificate,
)

router = APIRouter()


@router.get("/certificates/verify/{verification_code}", response_model=CertificateVerificationResponse)
def get_verify_certificate(verification_code: str) -> CertificateVerificationResponse:
    # Endpoint publico (sin auth) para validar un certificado compartido.
    return verify_certificate(verification_code)


@router.post("/final", response_model=FinalExamAttemptResponse, status_code=201)
def post_final_exam(
    payload: StartFinalExamRequest,
    current_user=Depends(get_current_supabase_user),
) -> FinalExamAttemptResponse:
    return start_final_exam(current_user, payload)


@router.post("/final/{attempt_id}/submit", response_model=FinalExamAttemptResponse)
def post_submit_final_exam(
    attempt_id: str,
    payload: SubmitFinalExamRequest,
    current_user=Depends(get_current_supabase_user),
) -> FinalExamAttemptResponse:
    return submit_final_exam(current_user, attempt_id, payload)


@router.get("/certificates/mine", response_model=list[CertificateResponse])
def get_my_certificates(current_user=Depends(get_current_supabase_user)) -> list[CertificateResponse]:
    return list_my_certificates(current_user)
