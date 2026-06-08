from fastapi import APIRouter, Depends

from app.core.security import get_current_supabase_user
from app.models.session import (
    EvaluationSubmissionRequest,
    FreeQuestionRequest,
    IntegrityEventRequest,
    LearningSessionResponse,
    MandatoryAnswerRequest,
    SessionSurveyRequest,
    StartLearningSessionRequest,
)
from app.models.orchestration import CompleteLessonResponse
from app.models.tutor import (
    LessonChatMessage,
    LessonChatRequest,
    LessonChatResponse,
    SuggestedQuestionsResponse,
)
from app.services.lesson_tutor_service import (
    ask_tutor,
    get_chat_history,
    get_suggested_questions,
)
from app.services.orchestrator_service import complete_lesson
from app.services.session_service import (
    answer_free_question,
    get_learning_session,
    record_integrity_event,
    start_learning_session,
    submit_mandatory_answer,
    submit_session_evaluation,
    submit_session_survey,
)

router = APIRouter()


@router.post("", response_model=LearningSessionResponse, status_code=201)
def post_session(
    payload: StartLearningSessionRequest,
    current_user=Depends(get_current_supabase_user),
) -> LearningSessionResponse:
    return start_learning_session(current_user, payload)


@router.get("/{session_id}", response_model=LearningSessionResponse)
def get_session(session_id: str, current_user=Depends(get_current_supabase_user)) -> LearningSessionResponse:
    return get_learning_session(current_user, session_id)


@router.post("/{session_id}/mandatory-answer", response_model=LearningSessionResponse)
def post_mandatory_answer(
    session_id: str,
    payload: MandatoryAnswerRequest,
    current_user=Depends(get_current_supabase_user),
) -> LearningSessionResponse:
    return submit_mandatory_answer(current_user, session_id, payload)


@router.post("/{session_id}/free-question", response_model=LearningSessionResponse)
def post_free_question(
    session_id: str,
    payload: FreeQuestionRequest,
    current_user=Depends(get_current_supabase_user),
) -> LearningSessionResponse:
    return answer_free_question(current_user, session_id, payload)


@router.post("/{session_id}/evaluation", response_model=LearningSessionResponse)
def post_evaluation(
    session_id: str,
    payload: EvaluationSubmissionRequest,
    current_user=Depends(get_current_supabase_user),
) -> LearningSessionResponse:
    return submit_session_evaluation(current_user, session_id, payload)


@router.post("/{session_id}/survey", response_model=LearningSessionResponse)
def post_survey(
    session_id: str,
    payload: SessionSurveyRequest,
    current_user=Depends(get_current_supabase_user),
) -> LearningSessionResponse:
    return submit_session_survey(current_user, session_id, payload)


@router.post("/{session_id}/integrity-event")
def post_integrity_event(
    session_id: str,
    payload: IntegrityEventRequest,
    current_user=Depends(get_current_supabase_user),
) -> dict:
    return record_integrity_event(current_user, session_id, payload)


# --- Tutor por leccion (Gini Eval) -----------------------------------------


@router.post("/{session_id}/lessons/{lesson_id}/chat", response_model=LessonChatResponse)
def post_lesson_chat(
    session_id: str,
    lesson_id: str,
    payload: LessonChatRequest,
    current_user=Depends(get_current_supabase_user),
) -> LessonChatResponse:
    return ask_tutor(current_user, lesson_id, payload.question, session_id=session_id)


@router.get(
    "/{session_id}/lessons/{lesson_id}/chat",
    response_model=list[LessonChatMessage],
)
def get_lesson_chat(
    session_id: str,
    lesson_id: str,
    current_user=Depends(get_current_supabase_user),
) -> list[LessonChatMessage]:
    return get_chat_history(current_user, lesson_id)


@router.get(
    "/{session_id}/lessons/{lesson_id}/suggested-questions",
    response_model=SuggestedQuestionsResponse,
)
def get_lesson_suggested_questions(
    session_id: str,
    lesson_id: str,
    current_user=Depends(get_current_supabase_user),
) -> SuggestedQuestionsResponse:
    return get_suggested_questions(current_user, lesson_id)


@router.post(
    "/{session_id}/lessons/{lesson_id}/complete",
    response_model=CompleteLessonResponse,
)
def post_complete_lesson(
    session_id: str,
    lesson_id: str,
    current_user=Depends(get_current_supabase_user),
) -> CompleteLessonResponse:
    # Gini Router orquesta: progreso -> insight -> coach -> proximo paso.
    return complete_lesson(current_user, session_id, lesson_id)
