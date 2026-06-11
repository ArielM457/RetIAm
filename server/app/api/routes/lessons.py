"""Tutor por leccion SIN sesion (para la pagina de lectura del curso).

El catalogo permite abrir un curso y leer su contenido directamente, sin generar
una ruta ni iniciar una sesion guiada. El tutor (Gini Eval) funciona igual: el
servicio trabaja por leccion y el session_id es opcional. Estos endpoints exponen
el mismo tutor sin requerir una sesion.
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.tutor import (
    LessonChatMessage,
    LessonChatRequest,
    LessonChatResponse,
    LessonReviewRequest,
    LessonReviewResponse,
    SuggestedQuestionsResponse,
)
from app.services.lesson_tutor_service import (
    ask_tutor,
    get_chat_history,
    get_suggested_questions,
    review_explanation,
)

router = APIRouter()


@router.post("/{lesson_id}/chat", response_model=LessonChatResponse)
def post_lesson_chat(
    lesson_id: str,
    payload: LessonChatRequest,
    current_user=Depends(get_current_supabase_user),
) -> LessonChatResponse:
    return ask_tutor(current_user, lesson_id, payload.question, session_id=None)


@router.get("/{lesson_id}/chat", response_model=list[LessonChatMessage])
def get_lesson_chat(
    lesson_id: str,
    current_user=Depends(get_current_supabase_user),
) -> list[LessonChatMessage]:
    return get_chat_history(current_user, lesson_id)


@router.get("/{lesson_id}/suggested-questions", response_model=SuggestedQuestionsResponse)
def get_lesson_suggested_questions(
    lesson_id: str,
    current_user=Depends(get_current_supabase_user),
) -> SuggestedQuestionsResponse:
    return get_suggested_questions(current_user, lesson_id)


@router.post("/{lesson_id}/review", response_model=LessonReviewResponse)
def post_lesson_review(
    lesson_id: str,
    payload: LessonReviewRequest,
    current_user=Depends(get_current_supabase_user),
) -> LessonReviewResponse:
    return review_explanation(
        current_user,
        lesson_id,
        payload.explanation,
        part_title=payload.part_title,
        technique=payload.technique,
    )
