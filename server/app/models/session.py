from typing import Literal

from pydantic import BaseModel, Field

from app.models.certification import ResourceReference


class StartLearningSessionRequest(BaseModel):
    plan_id: str
    section_id: str
    section_title: str
    session_type: Literal["theory", "practice", "quiz", "lab"] = "theory"


class SessionQuestion(BaseModel):
    prompt: str
    answer: str
    source: str


class MandatoryAnswerRequest(BaseModel):
    answer: str


class FreeQuestionRequest(BaseModel):
    question: str


class QuizAnswer(BaseModel):
    question_id: str
    selected_option_index: int


class EvaluationSubmissionRequest(BaseModel):
    # quiz_answers: respuestas elegidas, calificadas en el servidor contra la clave.
    quiz_answers: list[QuizAnswer] | None = None
    # answers: compatibilidad hacia atras (ya no se confia en is_correct del cliente).
    answers: list[dict] | None = None
    lab_solution_summary: str | None = None


class SessionSurveyRequest(BaseModel):
    skipped: bool = False
    clarity_score: int | None = Field(default=None, ge=1, le=5)
    preferred_format: str | None = None
    improvement_note: str | None = None


class IntegrityEventRequest(BaseModel):
    event_type: str
    payload: dict = Field(default_factory=dict)


class LearningSessionResponse(BaseModel):
    id: str | None = None
    plan_id: str
    section_id: str
    section_title: str
    session_type: str
    status: str
    resources: list[ResourceReference] = Field(default_factory=list)
    mandatory_question: SessionQuestion | None = None
    free_questions: list[dict] = Field(default_factory=list)
    evaluation: dict = Field(default_factory=dict)
    survey: dict | None = None
    started_at: str | None = None
    completed_at: str | None = None
