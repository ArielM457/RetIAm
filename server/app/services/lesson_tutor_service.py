"""Tutor por leccion con RAG (Gini Eval).

El tutor recupera fragmentos reales del contenido completo de las lecciones desde
Supabase pgvector (rag_service) y los pasa como CONTEXTO a GPT-4o con un prompt
estricto: responde solo con ese contexto, sin inventar. Ya no se inyecta el
resumen de la leccion en la consulta.

Degrada con gracia:
- Con Foundry + chunks: respuesta generada y fundamentada con citas.
- Sin Foundry pero con chunks: respuesta extractiva (el fragmento mas relevante).
- Sin chunks (RAG no ingerido): mensaje honesto de que no hay material indexado.
"""

import json
import logging

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import run_agent, run_agent_json
from app.models.course import CourseLesson, LessonSource
from app.models.tutor import (
    LessonChatMessage,
    LessonChatResponse,
    SuggestedQuestionsResponse,
)
from app.services import rag_service
from app.services._shared import response_data
from app.services.course_service import require_lesson_context
from app.services.profile_service import ensure_profile_for_user

logger = logging.getLogger(__name__)


def _client():
    return get_supabase_service_client()


def _persist_message(
    user_id: str,
    lesson_id: str,
    session_id: str | None,
    role: str,
    content: str,
    sources: list[dict],
    suggested: list[str],
    source_mode: str,
) -> dict:
    settings = get_settings()
    return response_data(
        _client()
        .table(settings.supabase_lesson_chat_messages_table)
        .insert(
            {
                "user_id": user_id,
                "lesson_id": lesson_id,
                "session_id": session_id,
                "role": role,
                "content": content,
                "sources": sources,
                "suggested_questions": suggested,
                "source_mode": source_mode,
            }
        )
        .execute(),
        [],
    )[0]


def _to_message(row: dict) -> LessonChatMessage:
    return LessonChatMessage(
        id=row.get("id"),
        role=row["role"],
        content=row["content"],
        sources=[LessonSource.model_validate(item) for item in (row.get("sources") or [])],
        suggested_questions=row.get("suggested_questions") or [],
        source_mode=row.get("source_mode", "mock"),
        created_at=row.get("created_at"),
    )


def _load_history(user_id: str, lesson_id: str) -> list[LessonChatMessage]:
    settings = get_settings()
    rows = response_data(
        _client()
        .table(settings.supabase_lesson_chat_messages_table)
        .select("*")
        .eq("user_id", user_id)
        .eq("lesson_id", lesson_id)
        .order("created_at")
        .execute(),
        [],
    ) or []
    return [_to_message(row) for row in rows]


def _chunks_to_sources(chunks: list[dict]) -> list[dict]:
    sources: list[dict] = []
    seen: set = set()
    for chunk in chunks:
        url = chunk.get("source_url")
        key = url or chunk.get("lesson_title")
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {"title": chunk.get("lesson_title") or "Material del curso", "url": url, "source": "rag"}
        )
    return sources


def _build_context(chunks: list[dict]) -> str:
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        title = chunk.get("lesson_title") or "Fragmento"
        blocks.append(f"[Fragmento {index} — {title}]\n{chunk.get('content', '')}")
    return "\n\n".join(blocks)


def _fallback_suggested_questions(lesson: CourseLesson) -> list[str]:
    questions = [f"¿Cuál es la idea principal de '{lesson.title}'?"]
    for objective in (lesson.learning_objectives or [])[:2]:
        questions.append(f"¿Puedes explicar más sobre: {objective}?")
    questions.append(f"¿Cómo se aplica '{lesson.title}' en un caso real?")
    return questions[:4]


def _parse_inline_suggestions(text: str) -> list[str]:
    if "SUGERENCIAS:" not in text:
        return []
    tail = text.split("SUGERENCIAS:", 1)[1].strip()
    try:
        data = json.loads(tail)
        if isinstance(data, list):
            return [str(item) for item in data][:4]
    except json.JSONDecodeError:
        parts = [part.strip("-• ").strip() for part in tail.replace("\n", ";").split(";")]
        return [part for part in parts if part][:4]
    return []


def ask_tutor(
    auth_user: object,
    lesson_id: str,
    question: str,
    session_id: str | None = None,
) -> LessonChatResponse:
    profile = ensure_profile_for_user(auth_user)
    context = require_lesson_context(lesson_id)
    lesson: CourseLesson = context["lesson"]
    certification = context.get("certification_code")

    _persist_message(profile.id, lesson_id, session_id, "user", question, [], [], "mock")

    # 1. Recuperar contexto real del curso (RAG).
    chunks = rag_service.retrieve(certification, question, k=5)
    sources = _chunks_to_sources(chunks)

    if not chunks:
        answer_text = (
            "No encuentro material indexado para responder esa pregunta con seguridad. "
            "Es posible que el contenido de esta lección aún no esté cargado en la base de "
            "conocimiento. Te recomiendo revisar las fuentes oficiales de la lección."
        )
        source_mode = "mock"
        suggested = _fallback_suggested_questions(lesson)
    else:
        context_text = _build_context(chunks)
        prompt = (
            f"Eres Gini Eval, tutor de la certificación {certification}. Responde la pregunta "
            "del alumno USANDO EXCLUSIVAMENTE el CONTEXTO de abajo (material real del curso). "
            "Si la respuesta no está en el contexto, dilo claramente y NO inventes. Cita el "
            "material cuando corresponda.\n\n"
            f"CONTEXTO:\n{context_text}\n\n"
            f"PREGUNTA: {question}\n\n"
            "Responde en español, claro y conciso (máx 180 palabras). Al final agrega una línea "
            'que empiece con SUGERENCIAS: y una lista JSON de 3 preguntas de seguimiento.'
        )
        result = run_agent("gini-eval", prompt, temperature=0.2, max_tokens=600, ground=False)
        if result:
            text = result["text"]
            suggested = _parse_inline_suggestions(text) or _fallback_suggested_questions(lesson)
            answer_text = text.split("SUGERENCIAS:")[0].strip()
            source_mode = "foundry"
        else:
            # Sin Foundry: respuesta extractiva con el fragmento mas relevante.
            top = chunks[0].get("content", "")
            answer_text = (
                f"Según el material del curso:\n\n{top[:700]}"
                + ("…" if len(top) > 700 else "")
            )
            suggested = _fallback_suggested_questions(lesson)
            source_mode = "mock"

    answer_row = _persist_message(
        profile.id, lesson_id, session_id, "assistant", answer_text, sources, suggested, source_mode
    )
    return LessonChatResponse(
        lesson_id=lesson_id,
        answer=_to_message(answer_row),
        history=_load_history(profile.id, lesson_id),
    )


def get_chat_history(auth_user: object, lesson_id: str) -> list[LessonChatMessage]:
    profile = ensure_profile_for_user(auth_user)
    require_lesson_context(lesson_id)
    return _load_history(profile.id, lesson_id)


def get_suggested_questions(auth_user: object, lesson_id: str) -> SuggestedQuestionsResponse:
    ensure_profile_for_user(auth_user)
    context = require_lesson_context(lesson_id)
    lesson: CourseLesson = context["lesson"]
    certification = context.get("certification_code")

    chunks = rag_service.retrieve(certification, lesson.title, k=4)
    if chunks:
        context_text = _build_context(chunks)
        prompt = (
            f"Genera 4 preguntas breves y útiles que un alumno podría hacer sobre la lección "
            f"«{lesson.title}», basándote SOLO en este material:\n{context_text}\n\n"
            'Devuelve SOLO un objeto JSON: {"questions": ["...", "..."]}'
        )
        parsed = run_agent_json("gini-eval", prompt, temperature=0.4, max_tokens=400, ground=False)
        if parsed and isinstance(parsed.get("questions"), list) and parsed["questions"]:
            return SuggestedQuestionsResponse(
                lesson_id=lesson_id,
                questions=[str(item) for item in parsed["questions"]][:4],
                source_mode="foundry",
            )
    return SuggestedQuestionsResponse(
        lesson_id=lesson_id,
        questions=_fallback_suggested_questions(lesson),
        source_mode="mock",
    )
