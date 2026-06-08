"""Modelos del tutor por leccion (Fase 3)."""

from pydantic import BaseModel, Field

from app.models.course import LessonSource


class LessonChatRequest(BaseModel):
    question: str = Field(min_length=1)


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
