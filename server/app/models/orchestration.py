"""Modelos de orquestacion (Fase 6 - Gini Router)."""

from pydantic import BaseModel


class CompleteLessonResponse(BaseModel):
    lesson_id: str
    status: str = "completed"
    completed_lessons: int = 0
    total_lessons: int = 0
    progress_percent: int = 0
    insight_note: str | None = None
    coach_message: str | None = None
    coach_scheduled_for: str | None = None
    next_action: str = "continue"
    next_action_label: str | None = None
    source_mode: str = "mock"
