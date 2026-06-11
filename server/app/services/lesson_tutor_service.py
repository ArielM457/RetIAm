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
import re

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import run_agent, run_agent_json
from app.models.course import CourseLesson, LessonSource
from app.models.tutor import (
    LessonChatMessage,
    LessonChatResponse,
    LessonReviewResponse,
    SuggestedQuestionsResponse,
)
from app.services import rag_service
from app.services._shared import response_data
from app.services.course_service import require_lesson_context
from app.services.profile_service import ensure_profile_for_user

logger = logging.getLogger(__name__)

_STOPWORDS = {
    "de", "la", "el", "y", "que", "en", "a", "los", "las", "un", "una", "por", "para",
    "con", "del", "al", "se", "lo", "le", "su", "sus", "como", "pero", "mas", "más",
    "esta", "este", "esto", "esa", "ese", "soy", "eres", "fue", "son", "hay", "muy",
    "me", "mi", "tu", "te", "ya", "si", "sin", "o",
}


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


def _meaningful_tokens(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}", text.lower()))
    return {token for token in tokens if token not in _STOPWORDS}


def _looks_related(explanation: str, context_text: str, lesson_title: str, subject: str | None) -> bool:
    explanation_tokens = _meaningful_tokens(explanation)
    if not explanation_tokens:
        return False

    context_tokens = _meaningful_tokens(f"{context_text}\n{lesson_title}\n{subject or ''}")
    overlap = explanation_tokens & context_tokens
    if overlap:
        return True

    # Fallback flexible: aceptar variaciones cercanas como singular/plural o tokens compuestos.
    for token in explanation_tokens:
        for candidate in context_tokens:
            if len(candidate) < 5:
                continue
            if token in candidate or candidate in token:
                return True
    return False


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

    try:
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
    except Exception as exc:
        logger.warning("Fallo get_suggested_questions para %s; se usa fallback: %s", lesson_id, exc)

    return SuggestedQuestionsResponse(
        lesson_id=lesson_id,
        questions=_fallback_suggested_questions(lesson),
        source_mode="mock",
    )


def review_explanation(
    auth_user: object,
    lesson_id: str,
    explanation: str,
    part_title: str | None = None,
    technique: str | None = None,
) -> LessonReviewResponse:
    ensure_profile_for_user(auth_user)
    context = require_lesson_context(lesson_id)
    lesson: CourseLesson = context["lesson"]
    certification = context.get("certification_code")
    subject = part_title or lesson.title

    chunks = rag_service.retrieve(certification, f"{lesson.title} {subject}", k=4)
    lesson_context_text = lesson.content_md or ""
    base_context_text = lesson_context_text
    if chunks:
        base_context_text = _build_context(chunks)

    related = _looks_related(explanation, base_context_text, lesson.title, subject)

    if not chunks:
        if related:
            return LessonReviewResponse(
                lesson_id=lesson_id,
                accepted=True,
                feedback="Tu explicacion si va con el tema de esta parte. Puedes continuar.",
                reinforcement="Buen trabajo. Si quieres mejorarla, menciona tambien la herramienta o el riesgo principal que se explica aqui.",
                source_mode="mock",
            )
        return LessonReviewResponse(
            lesson_id=lesson_id,
            accepted=False,
            feedback="Todavia no puedo validar esta explicacion con el contexto de esta parte. Intenta responder usando la idea principal del texto.",
            reinforcement="Si vuelve a pasar, revisa el contenido una vez mas y resume solo lo que se explica en esta parte.",
            source_mode="mock",
        )

    context_text = _build_context(chunks)
    if not related:
        return LessonReviewResponse(
            lesson_id=lesson_id,
            accepted=False,
            feedback="Eso no tiene que ver con esta parte. Intenta otra vez enfocandote en la idea principal del texto.",
            reinforcement="Usa palabras simples, pero habla solo de lo que acabas de leer en esta parte.",
            source_mode="mock",
        )

    prompt = (
        "Eres Gini Eval revisando una explicacion breve de un alumno sobre una parte de una leccion. "
        "Debes ser amable, rapido y muy claro. SOLO rechaza si la respuesta no tiene relacion con el contenido o es claramente absurda. "
        "Si la idea es razonable, aceptala aunque sea incompleta. Cuando aceptes, responde con un tono positivo, di brevemente que va bien y agrega un detalle interesante o util para reforzar. "
        "Cuando rechaces, di claramente que no tiene que ver con esta parte y pide que lo intente otra vez con la idea principal.\n\n"
        f"LECCION: {lesson.title}\n"
        f"PARTE: {subject}\n"
        f"METODOLOGIA: {technique or 'general'}\n\n"
        f"CONTEXTO DEL CURSO:\n{context_text}\n\n"
        f"EXPLICACION DEL ALUMNO:\n{explanation}\n\n"
        'Devuelve SOLO JSON con esta forma: {"accepted": true, "feedback": "...", "reinforcement": "..."}'
    )
    parsed = run_agent_json("gini-eval", prompt, temperature=0.2, max_tokens=300, ground=False)
    if parsed:
        accepted = bool(parsed.get("accepted", True))
        if accepted and not related:
            accepted = False
        feedback = str(parsed.get("feedback") or "").strip() or (
            "Vas bien, tu explicacion esta alineada con el contenido. Puedes continuar."
            if accepted
            else "Eso no tiene que ver con esta parte. Intenta otra vez enfocandote en la idea principal del texto."
        )
        reinforcement = str(parsed.get("reinforcement") or "").strip() or None
        return LessonReviewResponse(
            lesson_id=lesson_id,
            accepted=accepted,
            feedback=feedback,
            reinforcement=reinforcement,
            source_mode="foundry",
        )

    return LessonReviewResponse(
        lesson_id=lesson_id,
        accepted=False,
        feedback="No pude confirmar que esta respuesta este alineada con esta parte. Intenta otra vez con un resumen mas centrado en el contenido.",
        reinforcement="Menciona la idea principal o algun concepto puntual que aparezca en el texto de esta parte.",
        source_mode="mock",
    )
