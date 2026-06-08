"""Acceso al catalogo de cursos (Fase 0).

Lectura para el catalogo y el tutor por leccion, y upsert idempotente usado por
la ingesta de contenido (Fase 1) y la generacion con plantillas (Fase 2).
"""

import logging

from fastapi import HTTPException

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.course import (
    CourseCatalogSummary,
    CourseDetail,
    CourseLab,
    CourseLesson,
    CourseSectionContent,
)
from app.services._shared import response_data

logger = logging.getLogger(__name__)


def _client():
    return get_supabase_service_client()


def _assemble_course(course_row: dict) -> CourseDetail:
    settings = get_settings()
    sections_rows = response_data(
        _client()
        .table(settings.supabase_course_sections_table)
        .select("*")
        .eq("course_id", course_row["id"])
        .order("order")
        .execute(),
        [],
    ) or []

    sections: list[CourseSectionContent] = []
    for section_row in sections_rows:
        lessons_rows = response_data(
            _client()
            .table(settings.supabase_course_lessons_table)
            .select("*")
            .eq("section_id", section_row["id"])
            .order("order")
            .execute(),
            [],
        ) or []
        labs_rows = response_data(
            _client()
            .table(settings.supabase_course_labs_table)
            .select("*")
            .eq("section_id", section_row["id"])
            .execute(),
            [],
        ) or []
        sections.append(
            CourseSectionContent(
                id=section_row["id"],
                course_id=section_row["course_id"],
                section_key=section_row["section_key"],
                title=section_row["title"],
                summary=section_row.get("summary"),
                order=section_row.get("order", 1),
                duration_minutes=section_row.get("duration_minutes", 0),
                lessons=[CourseLesson.model_validate(item) for item in lessons_rows],
                labs=[CourseLab.model_validate(item) for item in labs_rows],
            )
        )

    return CourseDetail(
        id=course_row["id"],
        certification_code=course_row["certification_code"],
        track=course_row["track"],
        title=course_row["title"],
        summary=course_row.get("summary"),
        provider=course_row.get("provider"),
        level=course_row.get("level", "basic"),
        total_duration_minutes=course_row.get("total_duration_minutes", 0),
        source=course_row.get("source", "template"),
        source_url=course_row.get("source_url"),
        sections=sections,
    )


def list_courses() -> list[CourseCatalogSummary]:
    settings = get_settings()
    try:
        course_rows = response_data(
            _client().table(settings.supabase_courses_table).select("*").execute(), []
        ) or []
    except Exception as exc:
        logger.warning("No se pudo listar el catalogo de cursos: %s", exc)
        return []

    summaries: list[CourseCatalogSummary] = []
    for course_row in course_rows:
        section_rows = response_data(
            _client()
            .table(settings.supabase_course_sections_table)
            .select("id")
            .eq("course_id", course_row["id"])
            .execute(),
            [],
        ) or []
        section_ids = [row["id"] for row in section_rows]
        lesson_count = 0
        if section_ids:
            lesson_rows = response_data(
                _client()
                .table(settings.supabase_course_lessons_table)
                .select("id")
                .in_("section_id", section_ids)
                .execute(),
                [],
            ) or []
            lesson_count = len(lesson_rows)
        summaries.append(
            CourseCatalogSummary(
                id=course_row["id"],
                certification_code=course_row["certification_code"],
                track=course_row["track"],
                title=course_row["title"],
                summary=course_row.get("summary"),
                provider=course_row.get("provider"),
                level=course_row.get("level", "basic"),
                total_duration_minutes=course_row.get("total_duration_minutes", 0),
                section_count=len(section_ids),
                lesson_count=lesson_count,
            )
        )
    return summaries


def get_course_detail(certification_code: str) -> CourseDetail | None:
    settings = get_settings()
    try:
        rows = response_data(
            _client()
            .table(settings.supabase_courses_table)
            .select("*")
            .eq("certification_code", certification_code)
            .limit(1)
            .execute(),
            [],
        ) or []
    except Exception as exc:
        logger.warning("Lookup de curso fallo para %s: %s", certification_code, exc)
        return None
    if not rows:
        return None
    return _assemble_course(rows[0])


def get_lesson_with_context(lesson_id: str) -> dict | None:
    """Devuelve la leccion con el contexto de su seccion y curso para grounding."""
    settings = get_settings()
    lesson_rows = response_data(
        _client()
        .table(settings.supabase_course_lessons_table)
        .select("*")
        .eq("id", lesson_id)
        .limit(1)
        .execute(),
        [],
    ) or []
    if not lesson_rows:
        return None
    lesson = lesson_rows[0]
    section_rows = response_data(
        _client()
        .table(settings.supabase_course_sections_table)
        .select("*")
        .eq("id", lesson["section_id"])
        .limit(1)
        .execute(),
        [],
    ) or []
    section = section_rows[0] if section_rows else {}
    course = {}
    if section:
        course_rows = response_data(
            _client()
            .table(settings.supabase_courses_table)
            .select("*")
            .eq("id", section["course_id"])
            .limit(1)
            .execute(),
            [],
        ) or []
        course = course_rows[0] if course_rows else {}
    return {
        "lesson": CourseLesson.model_validate(lesson),
        "section_title": section.get("title"),
        "certification_code": course.get("certification_code"),
        "course_title": course.get("title"),
    }


def require_lesson_context(lesson_id: str) -> dict:
    context = get_lesson_with_context(lesson_id)
    if not context:
        raise HTTPException(status_code=404, detail="Leccion no encontrada.")
    return context


def upsert_course(course: CourseDetail) -> str:
    """Inserta o actualiza un curso completo de forma idempotente.

    Idempotencia por: certification_code (course), (course_id, section_key),
    (section_id, lesson_key), (section_id, lab_key). Usado por la ingesta.
    """
    settings = get_settings()
    course_payload = {
        "certification_code": course.certification_code,
        "track": course.track,
        "title": course.title,
        "summary": course.summary,
        "provider": course.provider,
        "level": course.level,
        "total_duration_minutes": course.total_duration_minutes,
        "source": course.source,
        "source_url": course.source_url,
    }
    course_row = response_data(
        _client()
        .table(settings.supabase_courses_table)
        .upsert(course_payload, on_conflict="certification_code")
        .execute(),
        [],
    )[0]
    course_id = course_row["id"]

    for section in course.sections:
        section_payload = {
            "course_id": course_id,
            "section_key": section.section_key,
            "title": section.title,
            "summary": section.summary,
            "order": section.order,
            "duration_minutes": section.duration_minutes,
        }
        section_row = response_data(
            _client()
            .table(settings.supabase_course_sections_table)
            .upsert(section_payload, on_conflict="course_id,section_key")
            .execute(),
            [],
        )[0]
        section_id = section_row["id"]

        for lesson in section.lessons:
            lesson_payload = {
                "section_id": section_id,
                "lesson_key": lesson.lesson_key,
                "title": lesson.title,
                "order": lesson.order,
                "duration_minutes": lesson.duration_minutes,
                "content_md": lesson.content_md,
                "learning_objectives": lesson.learning_objectives,
                "sources": [source.model_dump() for source in lesson.sources],
            }
            _client().table(settings.supabase_course_lessons_table).upsert(
                lesson_payload, on_conflict="section_id,lesson_key"
            ).execute()

        for lab in section.labs:
            lab_payload = {
                "section_id": section_id,
                "lab_key": lab.lab_key,
                "title": lab.title,
                "is_optional": lab.is_optional,
                "estimated_minutes": lab.estimated_minutes,
                "instructions_md": lab.instructions_md,
                "rubric": [criterion.model_dump() for criterion in lab.rubric],
            }
            _client().table(settings.supabase_course_labs_table).upsert(
                lab_payload, on_conflict="section_id,lab_key"
            ).execute()

    return course_id
