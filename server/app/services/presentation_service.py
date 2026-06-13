"""Sala de Auxiliaturas (Sala 1).

Genera una presentación (deck de slides) sobre un tema de un curso, fundamentada
en el contenido real del curso (RAG sobre pgvector). Verifica que el tema
pertenezca a ESE curso (los fragmentos se filtran por certification_code).

Degrada con gracia:
- Con Foundry + chunks: deck generado por el modelo (gpt-4.1-mini si está configurado).
- Sin Foundry pero con chunks: deck extractivo a partir de los fragmentos.
- Sin chunks: mensaje honesto (tema no indexado / no pertenece al curso).
"""

import logging

from app.core.config import get_settings
from app.integrations.foundry_adapter import run_agent, run_agent_json
from app.models.presentation import PresentationResponse, Slide
from app.services import rag_service
from app.services.course_service import get_course_detail
from app.services.profile_service import ensure_profile_for_user

logger = logging.getLogger(__name__)

# Umbral de similitud (coseno) para considerar que el tema sí está en el curso.
_MIN_SIMILARITY = 0.80

# Especificación del JSON de slides (reutilizada por varias funciones).
_SLIDES_JSON_SPEC = (
    "Devuelve SOLO un objeto JSON con esta forma exacta:\n"
    '{"title": "título de la clase", "slides": [\n'
    '  {"title": "título del slide", "bullets": ["punto 1", "punto 2"],\n'
    '   "code": "ejemplo de código SOLO si el tema es técnico y lo amerita, si no omítelo",\n'
    '   "diagram": ["Paso 1", "Paso 2", "Paso 3"],\n'
    '   "narration": "lo que dirías en voz alta para explicar este slide"}\n'
    "]}\n\n"
    "Reglas: 4 a 7 slides, en español, claro y didáctico. La 'narration' debe ser "
    "conversacional (se leerá en voz alta). Haz los slides VARIADOS e interactivos:\n"
    "- 'code': inclúyelo SOLO cuando el tema sea técnico y un ejemplo de comando/config aporte. "
    "No lo pongas en todos los slides.\n"
    "- 'diagram': un arreglo de 3 a 5 pasos cortos SOLO cuando el slide explique un PROCESO o "
    "FLUJO (p. ej. pasos de configuración). Si no es un flujo, omítelo o déjalo vacío.\n"
    "- La mayoría de slides deben apoyarse en 'bullets'. Un mismo slide normalmente NO lleva "
    "'code' y 'diagram' a la vez."
)


def _parse_slides(parsed: dict | None, topic: str) -> list[Slide]:
    """Convierte la respuesta JSON del modelo en objetos Slide."""
    if not parsed or not isinstance(parsed.get("slides"), list):
        return []
    slides: list[Slide] = []
    for item in parsed["slides"]:
        if not isinstance(item, dict):
            continue
        diagram = item.get("diagram") or []
        slides.append(
            Slide(
                title=str(item.get("title") or topic),
                bullets=[str(b) for b in (item.get("bullets") or [])],
                code=(str(item["code"]) if item.get("code") else None),
                diagram=[str(s) for s in diagram if str(s).strip()][:5]
                if isinstance(diagram, list)
                else [],
                narration=str(item.get("narration") or ""),
            )
        )
    return slides


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


def _fallback_slides(chunks: list[dict], topic: str) -> list[Slide]:
    """Deck extractivo si no hay Foundry: un slide por fragmento relevante."""
    slides = [
        Slide(
            title=f"{topic}",
            bullets=["Resumen a partir del material del curso."],
            narration="Veamos este tema con el material del curso.",
        )
    ]
    for chunk in chunks[:4]:
        text = (chunk.get("content") or "").strip()
        slides.append(
            Slide(
                title=chunk.get("lesson_title") or "Detalle",
                bullets=[text[:280] + ("…" if len(text) > 280 else "")],
                narration=text[:400],
            )
        )
    return slides


def generate_presentation(
    auth_user: object, course_code: str | None, topic: str
) -> PresentationResponse:
    ensure_profile_for_user(auth_user)

    # course_code opcional: vacío/None ⇒ RAG global (todos los cursos).
    code = (course_code or "").strip() or None
    course_title = "todos los cursos"
    if code:
        course = get_course_detail(code)
        if course:
            course_title = course.title
        else:
            code = None  # código inválido ⇒ buscamos en todos

    chunks = rag_service.retrieve(code, topic, k=6)
    sources = _chunks_to_sources(chunks)
    top_similarity = float(chunks[0].get("similarity") or 0) if chunks else 0.0
    grounded = bool(chunks) and top_similarity >= _MIN_SIMILARITY

    settings = get_settings()
    scope = f"el curso «{course_title}»" if code else "el catálogo de cursos"

    if chunks:
        context = _build_context(chunks)
        source_rules = (
            "Apóyate PRINCIPALMENTE en el CONTEXTO de abajo (material real de los cursos). "
            "Si el contexto no cubre todo el tema, puedes complementarlo con tu conocimiento, "
            "pero SOLO con información correcta de fuentes oficiales (Microsoft Learn, AWS docs, "
            "documentación oficial del proveedor). No inventes.\n\n"
            f"CONTEXTO:\n{context}\n\n"
        )
        warning = (
            None
            if grounded
            else "Complementé con conocimiento general porque el material del curso "
            "cubría poco este tema."
        )
    else:
        # Sin material indexado: el modelo responde con su conocimiento (fuentes confiables).
        context = ""
        source_rules = (
            "No hay material indexado de los cursos para este tema. Respóndelo con TU "
            "conocimiento, pero basándote en información correcta de FUENTES OFICIALES y "
            "confiables (Microsoft Learn, documentación oficial de Azure/AWS/GitHub). Sé "
            "preciso y práctico; NO inventes comandos ni nombres de servicios.\n\n"
        )
        warning = (
            "No encontré material indexado en los cursos para este tema; te respondo con "
            "conocimiento general basado en documentación oficial."
        )

    prompt = (
        f"Eres Gini Path, un auxiliar experto que ayuda a estudiantes sobre {scope}. "
        f"El alumno preguntó: «{topic}».\n\n"
        "Crea una PRESENTACIÓN clara y didáctica para responder/enseñar ese tema.\n\n"
        f"{source_rules}"
        f"{_SLIDES_JSON_SPEC}"
    )

    parsed = run_agent_json(
        "gini-path",
        prompt,
        temperature=0.3,
        max_tokens=1800,
        ground=False,
        deployment=settings.azure_foundry_deployment_presenter or None,
    )

    slides = _parse_slides(parsed, topic)
    if slides:
        return PresentationResponse(
            course_code=code or "ALL",
            topic=topic,
            title=str((parsed or {}).get("title") or topic),
            grounded=grounded,
            slides=slides,
            sources=sources,
            source_mode="foundry",
            message=warning,
        )

    # Sin Foundry (o respuesta inválida): si hay chunks, deck extractivo;
    # si no hay nada, mensaje honesto.
    if not chunks:
        return PresentationResponse(
            course_code=code or "ALL",
            topic=topic,
            title=topic,
            grounded=False,
            message=(
                "No pude generar la clase: no hay material indexado y la IA externa está "
                "desactivada. Activa ENABLE_EXTERNAL_AI o ingiere cursos con --rag."
            ),
        )

    return PresentationResponse(
        course_code=code or "ALL",
        topic=topic,
        title=topic,
        grounded=grounded,
        slides=_fallback_slides(chunks, topic),
        sources=sources,
        source_mode="mock",
        message=warning,
    )


def answer_question(
    auth_user: object, question: str, course_code: str | None = None, topic: str | None = None
) -> dict:
    """Responde una DUDA puntual durante la clase (sin regenerar la presentación).

    Devuelve {"answer": str, "sources": [...]}. Respuesta corta y conversacional
    (se leerá en voz alta). Usa el RAG (global o por curso) y cae a conocimiento
    general con fuentes oficiales si no hay material.
    """
    ensure_profile_for_user(auth_user)
    code = (course_code or "").strip() or None

    chunks = rag_service.retrieve(code, question, k=4)
    sources = _chunks_to_sources(chunks)
    settings = get_settings()

    if chunks:
        context = _build_context(chunks)
        rules = (
            "Apóyate en el CONTEXTO (material de los cursos); si no alcanza, complementa con "
            "conocimiento correcto de fuentes oficiales. No inventes.\n\n"
            f"CONTEXTO:\n{context}\n\n"
        )
    else:
        rules = (
            "No hay material indexado; responde con tu conocimiento basándote en fuentes "
            "oficiales (Microsoft Learn, documentación de Azure/AWS/GitHub). No inventes.\n\n"
        )

    tema = f' (en el contexto del tema «{topic}»)' if topic else ""
    prompt = (
        f"Eres Gini Path, el auxiliar del metaverso. El alumno te interrumpió con una DUDA{tema}: "
        f"«{question}».\n\n"
        f"{rules}"
        "Responde de forma BREVE y conversacional (2 a 4 frases, en español, para leer en voz "
        "alta). Ve directo al grano; no uses formato Markdown ni listas."
    )

    result = run_agent(
        "gini-path",
        prompt,
        temperature=0.3,
        max_tokens=400,
        ground=False,
        deployment=settings.azure_foundry_deployment_presenter or None,
    )
    if result and result.get("text"):
        return {"answer": result["text"].strip(), "sources": sources}

    # Fallback sin Foundry: el fragmento más relevante.
    if chunks:
        text = (chunks[0].get("content") or "").strip()
        return {"answer": text[:500] or "No encontré una respuesta clara.", "sources": sources}
    return {
        "answer": "Ahora mismo no puedo responder esa duda (la IA externa está desactivada).",
        "sources": [],
    }


def generate_from_text(
    auth_user: object, text: str, topic: str | None = None
) -> PresentationResponse:
    """Genera una presentación a partir de un TEXTO/artículo que sube el alumno."""
    ensure_profile_for_user(auth_user)
    material = (text or "").strip()
    asked = (topic or "").strip() or "este material"

    if not material:
        return PresentationResponse(
            course_code="UPLOAD",
            topic=asked,
            title=asked,
            grounded=False,
            message="No recibí ningún texto para explicar.",
        )

    settings = get_settings()
    prompt = (
        "Eres Gini Path, un auxiliar del metaverso. El alumno subió el siguiente MATERIAL y "
        f"quiere que se lo expliques{'' if not topic else f' (enfócate en: «{topic}»)'}.\n\n"
        f"MATERIAL:\n{material[:8000]}\n\n"
        "Crea una PRESENTACIÓN clara que explique y resuma este material para que el alumno lo "
        "entienda. Apóyate EN EL MATERIAL; puedes añadir contexto correcto si ayuda, sin "
        "contradecirlo.\n\n"
        f"{_SLIDES_JSON_SPEC}"
    )

    parsed = run_agent_json(
        "gini-path",
        prompt,
        temperature=0.3,
        max_tokens=1800,
        ground=False,
        deployment=settings.azure_foundry_deployment_presenter or None,
    )
    slides = _parse_slides(parsed, asked)
    if slides:
        return PresentationResponse(
            course_code="UPLOAD",
            topic=asked,
            title=str((parsed or {}).get("title") or f"Explicación: {asked}"),
            grounded=True,
            slides=slides,
            sources=[],
            source_mode="foundry",
            message="Presentación basada en el material que subiste.",
        )

    return PresentationResponse(
        course_code="UPLOAD",
        topic=asked,
        title=asked,
        grounded=False,
        message="No pude generar la clase desde el texto (¿IA externa desactivada?).",
    )
