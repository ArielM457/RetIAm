"""Cursos personalizados creados por un team lead.

Flujo: el lead sube/pega un Markdown con la estructura del curso. Lo normalizamos
a la jerarquia estandar (CourseDetail) con gpt-4.1-mini (con un parser
determinista de respaldo), validamos los minimos para que sea "certificable",
lo guardamos con scope del equipo (visible solo para sus miembros) y generamos
los embeddings de cada leccion en el pgvector de Supabase para que la IA pueda
responder dudas de ese tema (RAG), igual que con los cursos de Microsoft Learn.
"""

import logging
import re
import secrets

from app.core.config import get_settings
from app.integrations.foundry_adapter import run_agent_json
from app.models.course import (
    CourseDetail,
    CourseLab,
    CourseLesson,
    CourseSectionContent,
)
from app.services import rag_service
from app.services.course_service import get_course_detail, upsert_course
from app.services.embedding_service import embedding_available, embed_documents
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import _ensure_manager_access

logger = logging.getLogger(__name__)

# Minimos "recomendados" para que un curso sea elegible como certificable.
MIN_SECTIONS = 3
MIN_LESSONS = 3
MIN_LABS = 1
MIN_DURATION_MINUTES = 60
# (El examen de certificacion se genera en tiempo de examen: 10 preguntas, 70%.)
EXAM_QUESTIONS = 10
EXAM_PASS_PERCENT = 70


def _slug(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:48] or fallback


def _chunk_text(text: str, size: int = 1800, overlap: int = 200) -> list[str]:
    text = (text or "").strip()
    if len(text) <= size:
        return [text] if len(text) > 60 else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        piece = text[start : start + size].strip()
        if len(piece) > 60:
            chunks.append(piece)
        start += size - overlap
    return chunks


def _estimate_minutes(text: str) -> int:
    words = len((text or "").split())
    return max(5, round(words / 180))  # ~180 palabras/min de lectura


def _normalize_with_ai(markdown: str, title_hint: str | None) -> dict | None:
    settings = get_settings()
    prompt = (
        "Convierte el siguiente MATERIAL en Markdown en la estructura de un curso. "
        "Respeta el contenido del autor (no inventes temas nuevos), solo organizalo.\n\n"
        f"MATERIAL:\n{markdown[:10000]}\n\n"
        "Devuelve SOLO un objeto JSON con esta forma exacta:\n"
        '{"title": "titulo del curso", "summary": "resumen breve", '
        '"level": "basic|intermediate|advanced", "sections": [\n'
        '  {"title": "titulo de seccion", "summary": "resumen",\n'
        '   "lessons": [{"title": "titulo leccion", "content_md": "contenido en markdown", '
        '"objectives": ["obj1", "obj2"]}],\n'
        '   "labs": [{"title": "titulo lab", "instructions_md": "instrucciones", "optional": true}]}\n'
        "]}\n\n"
        "Reglas: en espanol; cada leccion debe conservar el contenido real (content_md); "
        "incluye labs solo si el material sugiere practica. No agregues secciones vacias."
    )
    if title_hint:
        prompt += f"\nEl titulo sugerido por el autor es: «{title_hint}»."
    return run_agent_json(
        "course-builder",
        prompt,
        temperature=0.2,
        max_tokens=3500,
        ground=False,
        deployment=settings.azure_foundry_deployment_presenter or None,
    )


def _parse_markdown_fallback(markdown: str, title_hint: str | None) -> dict:
    """Parser determinista por encabezados (respaldo si no hay IA).

    # Titulo  ·  ## Seccion  ·  ### Leccion (+contenido)  ·  #### Lab: ...
    """
    title = title_hint or "Curso personalizado"
    sections: list[dict] = []
    cur_section: dict | None = None
    cur_lesson: dict | None = None
    cur_lab: dict | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        text = "\n".join(buffer).strip()
        buffer = []
        if cur_lab is not None:
            cur_lab["instructions_md"] = (cur_lab.get("instructions_md") or "") + text
        elif cur_lesson is not None:
            cur_lesson["content_md"] = (cur_lesson.get("content_md") or "") + text

    for raw in (markdown or "").splitlines():
        line = raw.rstrip()
        if line.startswith("#### ") and line[5:].lower().lstrip().startswith("lab"):
            flush()
            cur_lab = {"title": line[5:].split(":", 1)[-1].strip() or "Laboratorio", "instructions_md": ""}
            cur_lesson = None
            if cur_section is not None:
                cur_section["labs"].append(cur_lab)
        elif line.startswith("### "):
            flush()
            cur_lab = None
            cur_lesson = {"title": line[4:].strip(), "content_md": "", "objectives": []}
            if cur_section is None:
                cur_section = {"title": "General", "summary": "", "lessons": [], "labs": []}
                sections.append(cur_section)
            cur_section["lessons"].append(cur_lesson)
        elif line.startswith("## "):
            flush()
            cur_lab = None
            cur_lesson = None
            cur_section = {"title": line[3:].strip(), "summary": "", "lessons": [], "labs": []}
            sections.append(cur_section)
        elif line.startswith("# "):
            flush()
            title = line[2:].strip() or title
        else:
            buffer.append(raw)
    flush()
    return {"title": title, "summary": "", "level": "basic", "sections": sections}


def _build_course_detail(parsed: dict, *, certification_code: str) -> CourseDetail:
    sections: list[CourseSectionContent] = []
    total_minutes = 0
    for s_idx, section in enumerate(parsed.get("sections") or [], start=1):
        if not isinstance(section, dict):
            continue
        s_key = f"seccion-{s_idx}-{_slug(section.get('title', ''), 's')}"
        lessons: list[CourseLesson] = []
        section_minutes = 0
        for l_idx, lesson in enumerate(section.get("lessons") or [], start=1):
            if not isinstance(lesson, dict):
                continue
            content = str(lesson.get("content_md") or "").strip()
            minutes = _estimate_minutes(content)
            section_minutes += minutes
            lessons.append(
                CourseLesson(
                    lesson_key=f"leccion-{s_idx}-{l_idx}-{_slug(lesson.get('title', ''), 'l')}",
                    title=str(lesson.get("title") or f"Leccion {s_idx}.{l_idx}"),
                    order=l_idx,
                    duration_minutes=minutes,
                    content_md=content or None,
                    learning_objectives=[str(o) for o in (lesson.get("objectives") or [])],
                )
            )
        labs: list[CourseLab] = []
        for b_idx, lab in enumerate(section.get("labs") or [], start=1):
            if not isinstance(lab, dict):
                continue
            labs.append(
                CourseLab(
                    lab_key=f"lab-{s_idx}-{b_idx}-{_slug(lab.get('title', ''), 'lab')}",
                    title=str(lab.get("title") or f"Laboratorio {s_idx}.{b_idx}"),
                    is_optional=bool(lab.get("optional", True)),
                    estimated_minutes=30,
                    instructions_md=str(lab.get("instructions_md") or "") or None,
                )
            )
        total_minutes += section_minutes
        sections.append(
            CourseSectionContent(
                section_key=s_key,
                title=str(section.get("title") or f"Seccion {s_idx}"),
                summary=str(section.get("summary") or "") or None,
                order=s_idx,
                duration_minutes=section_minutes,
                lessons=lessons,
                labs=labs,
            )
        )

    level = parsed.get("level") if parsed.get("level") in {"basic", "intermediate", "advanced"} else "basic"
    return CourseDetail(
        certification_code=certification_code,
        track="custom",
        title=str(parsed.get("title") or "Curso personalizado"),
        summary=str(parsed.get("summary") or "") or None,
        provider="Plataforma RetIAm",
        level=level,
        total_duration_minutes=total_minutes,
        source="custom",
        visibility="team",
        sections=sections,
    )


def validate_certifiable(course: CourseDetail) -> tuple[bool, list[str]]:
    """Comprueba los minimos recomendados para ser elegible como certificacion."""
    issues: list[str] = []
    section_count = len(course.sections)
    lesson_count = sum(len(s.lessons) for s in course.sections)
    lab_count = sum(len(s.labs) for s in course.sections)
    lessons_with_content = sum(
        1 for s in course.sections for le in s.lessons if (le.content_md or "").strip()
    )

    if section_count < MIN_SECTIONS:
        issues.append(f"Necesita al menos {MIN_SECTIONS} secciones (tiene {section_count}).")
    if lesson_count < MIN_LESSONS:
        issues.append(f"Necesita al menos {MIN_LESSONS} lecciones (tiene {lesson_count}).")
    if lab_count < MIN_LABS:
        issues.append(f"Necesita al menos {MIN_LABS} laboratorio (tiene {lab_count}).")
    if lessons_with_content < lesson_count or lesson_count == 0:
        issues.append("Todas las lecciones deben tener contenido (content_md).")
    if course.total_duration_minutes < MIN_DURATION_MINUTES:
        issues.append(
            f"La duracion estimada debe ser >= {MIN_DURATION_MINUTES} min "
            f"(tiene {course.total_duration_minutes})."
        )
    return (not issues), issues


def _course_summary(course: CourseDetail, is_certifiable: bool, issues: list[str]) -> dict:
    return {
        "certification_code": course.certification_code,
        "title": course.title,
        "summary": course.summary,
        "level": course.level,
        "total_duration_minutes": course.total_duration_minutes,
        "section_count": len(course.sections),
        "lesson_count": sum(len(s.lessons) for s in course.sections),
        "lab_count": sum(len(s.labs) for s in course.sections),
        "is_certifiable": is_certifiable,
        "issues": issues,
        "exam_questions": EXAM_QUESTIONS,
        "exam_pass_percent": EXAM_PASS_PERCENT,
        "sections": [
            {"title": s.title, "lessons": [le.title for le in s.lessons], "labs": [b.title for b in s.labs]}
            for s in course.sections
        ],
    }


def _parse_markdown(markdown: str, title_hint: str | None) -> dict:
    parsed = _normalize_with_ai(markdown, title_hint)
    if parsed and isinstance(parsed.get("sections"), list) and parsed["sections"]:
        return parsed
    logger.info("Normalizacion IA del curso personalizado no disponible; uso parser determinista.")
    return _parse_markdown_fallback(markdown, title_hint)


def preview_custom_course(
    auth_user: object, team_id: str, markdown: str, title: str | None = None
) -> dict:
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)
    parsed = _parse_markdown(markdown, title)
    course = _build_course_detail(parsed, certification_code="TEAM-PREVIEW")
    is_certifiable, issues = validate_certifiable(course)
    return _course_summary(course, is_certifiable, issues)


def create_custom_course(
    auth_user: object, team_id: str, markdown: str, title: str | None = None
) -> dict:
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)

    parsed = _parse_markdown(markdown, title)
    certification_code = _unique_code()
    course = _build_course_detail(parsed, certification_code=certification_code)
    course.team_id = team_id
    course.created_by = profile.id
    is_certifiable, issues = validate_certifiable(course)
    course.is_certifiable = is_certifiable

    upsert_course(course)
    chunk_count = _embed_course_lessons(course)

    result = _course_summary(course, is_certifiable, issues)
    result["chunk_count"] = chunk_count
    result["message"] = (
        "Curso creado y certificable. Tus miembros ya pueden tomarlo."
        if is_certifiable
        else "Curso creado como borrador (aun no certificable): revisa los puntos pendientes."
    )
    return result


def _unique_code() -> str:
    for _ in range(8):
        code = f"TEAM-{secrets.token_hex(3).upper()}"
        if not get_course_detail(code):
            return code
    return f"TEAM-{secrets.token_hex(4).upper()}"


def _embed_course_lessons(course: CourseDetail) -> int:
    """Genera embeddings de cada leccion y los guarda en el pgvector (RAG)."""
    if not embedding_available():
        logger.warning("fastembed no disponible: el curso personalizado no tendra RAG.")
        return 0
    total = 0
    for section in course.sections:
        for lesson in section.lessons:
            chunks = _chunk_text(lesson.content_md or "")
            if not chunks:
                continue
            try:
                embeddings = embed_documents(chunks)
                rag_service.upsert_lesson_chunks(
                    course.certification_code,
                    lesson.lesson_key,
                    lesson.title,
                    chunks,
                    embeddings,
                    None,
                )
                total += len(chunks)
            except Exception as exc:  # noqa: BLE001
                logger.warning("No se pudo embeber la leccion %s: %s", lesson.lesson_key, exc)
    return total
