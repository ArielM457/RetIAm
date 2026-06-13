"""Modelos de la Sala de Auxiliaturas (Sala 1).

Un agente genera una PRESENTACION (deck de slides) sobre un tema de un curso,
fundamentada en el contenido real (RAG). El robot del metaverso la mostrará en
una pantalla y narrará cada slide.
"""

from pydantic import BaseModel, Field

from app.models.course import LessonSource


class PresentationRequest(BaseModel):
    # Opcional: vacío/None = busca en TODOS los cursos (RAG global).
    course_code: str | None = None
    topic: str = Field(min_length=1)


class QuestionRequest(BaseModel):
    """Duda puntual del alumno durante la clase (no regenera la presentación)."""

    question: str = Field(min_length=1)
    course_code: str | None = None
    topic: str | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[LessonSource] = Field(default_factory=list)


class FromTextRequest(BaseModel):
    """El alumno sube/pega un texto o artículo para que la IA se lo explique."""

    text: str = Field(min_length=1)
    topic: str | None = None


class Slide(BaseModel):
    title: str
    bullets: list[str] = Field(default_factory=list)
    code: str | None = None          # ejemplo de código (solo si el tema lo amerita)
    diagram: list[str] = Field(default_factory=list)  # pasos de un flujo (solo si ayuda)
    narration: str = ""              # lo que dice el robot en ese slide (para TTS)


class PresentationResponse(BaseModel):
    course_code: str
    topic: str
    title: str
    grounded: bool                   # True si se fundamentó en contenido real del curso
    slides: list[Slide] = Field(default_factory=list)
    sources: list[LessonSource] = Field(default_factory=list)
    source_mode: str = "mock"        # "foundry" si lo generó el modelo; "mock" si fallback
    message: str | None = None       # aviso (p. ej. tema no encontrado en el curso)
