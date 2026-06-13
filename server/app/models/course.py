"""Modelos del catalogo de cursos (Fase 0).

Jerarquia de contenido global: Course -> CourseSection -> CourseLesson / CourseLab.
Estos modelos los pueblan la ingesta de MS Learn (Fase 1) y el motor de
generacion con plantillas (Fase 2), y los consume el tutor por leccion (Fase 3).
"""

from pydantic import BaseModel, Field


class LessonSource(BaseModel):
    """Cita de una fuente fundamentada para una leccion."""

    title: str
    url: str | None = None
    source: str | None = None


class RubricCriterion(BaseModel):
    """Criterio de evaluacion para un laboratorio."""

    criterion: str
    weight: int = 1
    description: str | None = None


class CourseLab(BaseModel):
    id: str | None = None
    section_id: str | None = None
    lesson_id: str | None = None
    lab_key: str
    title: str
    is_optional: bool = True
    estimated_minutes: int = 30
    instructions_md: str | None = None
    rubric: list[RubricCriterion] = Field(default_factory=list)


class CourseLesson(BaseModel):
    id: str | None = None
    section_id: str | None = None
    lesson_key: str
    title: str
    order: int = 1
    duration_minutes: int = 0
    content_md: str | None = None
    learning_objectives: list[str] = Field(default_factory=list)
    sources: list[LessonSource] = Field(default_factory=list)


class CourseSectionContent(BaseModel):
    id: str | None = None
    course_id: str | None = None
    section_key: str
    title: str
    summary: str | None = None
    order: int = 1
    duration_minutes: int = 0
    lessons: list[CourseLesson] = Field(default_factory=list)
    labs: list[CourseLab] = Field(default_factory=list)


class CourseDetail(BaseModel):
    id: str | None = None
    certification_code: str
    track: str
    title: str
    summary: str | None = None
    provider: str | None = None
    level: str = "basic"
    total_duration_minutes: int = 0
    source: str = "template"
    source_url: str | None = None
    # Cursos personalizados (team lead): scoping + certificacion de plataforma.
    team_id: str | None = None
    created_by: str | None = None
    visibility: str = "global"  # 'global' | 'team' | 'org'
    is_certifiable: bool = False
    sections: list[CourseSectionContent] = Field(default_factory=list)


class CustomCourseRequest(BaseModel):
    """El team lead sube/pega un Markdown para crear un curso personalizado."""

    markdown: str = Field(min_length=1)
    title: str | None = None


class CourseCatalogSummary(BaseModel):
    """Vista ligera para listar cursos sin traer todo el contenido."""

    id: str | None = None
    certification_code: str
    track: str
    title: str
    summary: str | None = None
    provider: str | None = None
    level: str = "basic"
    total_duration_minutes: int = 0
    section_count: int = 0
    lesson_count: int = 0
    # Para distinguir y marcar cursos personalizados del equipo en el catalogo.
    visibility: str = "global"
    is_certifiable: bool = False
    source: str = "template"
