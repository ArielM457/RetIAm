"""Sala de Auxiliaturas (Sala 1): generar una presentación de un tema de un curso."""

from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.presentation import (
    AnswerResponse,
    FromTextRequest,
    PresentationRequest,
    PresentationResponse,
    QuestionRequest,
)
from app.services.presentation_service import (
    answer_question,
    generate_from_text,
    generate_presentation,
)

router = APIRouter()


@router.post("", response_model=PresentationResponse)
def post_presentation(
    payload: PresentationRequest,
    current_user=Depends(get_current_supabase_user),
) -> PresentationResponse:
    return generate_presentation(current_user, payload.course_code, payload.topic)


@router.post("/ask", response_model=AnswerResponse)
def post_question(
    payload: QuestionRequest,
    current_user=Depends(get_current_supabase_user),
) -> AnswerResponse:
    """Responde una duda durante la clase sin regenerar la presentación."""
    result = answer_question(
        current_user, payload.question, payload.course_code, payload.topic
    )
    return AnswerResponse(**result)


@router.post("/from-text", response_model=PresentationResponse)
def post_from_text(
    payload: FromTextRequest,
    current_user=Depends(get_current_supabase_user),
) -> PresentationResponse:
    """Genera una presentación a partir de un texto/artículo que sube el alumno."""
    return generate_from_text(current_user, payload.text, payload.topic)
