"""Modelos del tutor por leccion (Fase 3)."""

from pydantic import BaseModel, Field

from app.models.course import LessonSource


class LessonChatRequest(BaseModel):
    question: str = Field(min_length=1)


class LessonReviewRequest(BaseModel):
    explanation: str = Field(min_length=1)
    part_title: str | None = None
    technique: str | None = None


class LessonChatMessage(BaseModel):
    id: str | None = None
    role: str
    content: str
    sources: list[LessonSource] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    source_mode: str = "mock"
    created_at: str | None = None


class LessonChatResponse(BaseModel):
    lesson_id: str
    answer: LessonChatMessage
    history: list[LessonChatMessage] = Field(default_factory=list)


class SuggestedQuestionsResponse(BaseModel):
    lesson_id: str
    questions: list[str] = Field(default_factory=list)
    source_mode: str = "mock"


class LessonReviewResponse(BaseModel):
    lesson_id: str
    accepted: bool
    feedback: str
    reinforcement: str | None = None
    source_mode: str = "mock"
