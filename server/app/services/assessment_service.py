"""Generacion y calificacion de evaluaciones (Fase 4).

Centraliza la creacion de preguntas de quiz y examen, y la calificacion de labs,
para que el avance dependa de respuestas correctas reales y no de flags enviados
por el cliente.

- Con Foundry activo: Gini Eval genera preguntas fundamentadas y califica labs.
- Sin Foundry: usa el banco de preguntas real de `onboarding_catalog` (preguntas
  con respuesta correcta) y una rubrica heuristica para labs.
"""

import logging

from app.integrations.foundry_adapter import run_agent_json
from app.services.onboarding_catalog import CERTIFICATION_TRACK_HINTS, QUESTION_BANK

logger = logging.getLogger(__name__)

PASS_THRESHOLD = 70


def resolve_track(certification: str) -> str:
    if certification in CERTIFICATION_TRACK_HINTS:
        return CERTIFICATION_TRACK_HINTS[certification]
    normalized = (certification or "").lower()
    if "aws" in normalized:
        return "aws"
    if "github" in normalized:
        return "github"
    return "azure"


def _bank_to_question(item: dict, question_id: str, section_id: str | None = None) -> dict:
    options = [opt["label"] for opt in item["options"]]
    correct_index = next(
        (idx for idx, opt in enumerate(item["options"]) if opt["key"] == item["correct_option_key"]),
        0,
    )
    return {
        "question_id": question_id,
        "prompt": item["prompt"],
        "options": options,
        "correct_option_index": correct_index,
        "source": item.get("topic", "banco"),
        "section_id": section_id,
    }


def _normalize_generated_questions(raw: list, id_prefix: str, section_id: str | None) -> list[dict]:
    questions: list[dict] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            continue
        options = item.get("options")
        correct = item.get("correct_option_index")
        if not isinstance(options, list) or len(options) < 2:
            continue
        if not isinstance(correct, int) or not (0 <= correct < len(options)):
            continue
        questions.append(
            {
                "question_id": f"{id_prefix}-{index}",
                "prompt": str(item.get("prompt", f"Pregunta {index}")),
                "options": [str(opt) for opt in options],
                "correct_option_index": correct,
                "source": str(item.get("source", "foundry_iq")),
                "section_id": section_id,
            }
        )
    return questions


def generate_quiz_questions(
    certification: str,
    section_title: str,
    content: str | None,
    *,
    n: int = 4,
    section_id: str | None = None,
) -> tuple[list[dict], str]:
    """Devuelve (questions, source_mode). Cada pregunta incluye correct_option_index."""
    prompt = (
        f"Genera {n} preguntas de opcion multiple (4 opciones) para evaluar la seccion "
        f"«{section_title}» de la certificacion {certification}. Basate en este contenido:\n"
        f"{(content or '')[:1500]}\n\n"
        'Devuelve SOLO JSON: {"questions":[{"prompt":"...","options":["a","b","c","d"],'
        '"correct_option_index":0,"source":"..."}]}'
    )
    parsed = run_agent_json("gini-eval", prompt, temperature=0.4, max_tokens=900)
    if parsed and isinstance(parsed.get("questions"), list):
        questions = _normalize_generated_questions(parsed["questions"], "quiz", section_id)
        if questions:
            return questions[:n], "foundry"

    track = resolve_track(certification)
    bank = QUESTION_BANK.get(track) or QUESTION_BANK["azure"]
    questions = [
        _bank_to_question(item, f"quiz-{index}", section_id)
        for index, item in enumerate(bank[:n], start=1)
    ]
    return questions, "mock"


def generate_exam_questions(
    certification: str,
    sections: list[dict],
    *,
    target_questions: int,
) -> tuple[list[dict], str]:
    """Genera preguntas de examen proporcionales por seccion. (questions, source_mode)."""
    section_titles = [section.get("title", section.get("section_id", "")) for section in sections]
    prompt = (
        f"Genera {target_questions} preguntas de opcion multiple (4 opciones) para el examen "
        f"final de {certification}, cubriendo proporcionalmente estas secciones: "
        f"{section_titles}. Devuelve SOLO JSON: "
        '{"questions":[{"prompt":"...","options":["a","b","c","d"],"correct_option_index":0,'
        '"section_id":"...","source":"..."}]}'
    )
    parsed = run_agent_json("gini-eval", prompt, temperature=0.4, max_tokens=2500)
    if parsed and isinstance(parsed.get("questions"), list):
        questions = _normalize_generated_questions(parsed["questions"], "exam", None)
        # asignar section_id si el agente no lo dio, repartiendo en orden
        if questions:
            for idx, question in enumerate(questions):
                if not question.get("section_id") and sections:
                    question["section_id"] = sections[idx % len(sections)].get("section_id")
            return questions[:target_questions], "foundry"

    # Fallback: banco real, repartido por seccion ciclicamente.
    track = resolve_track(certification)
    bank = QUESTION_BANK.get(track) or QUESTION_BANK["azure"]
    questions: list[dict] = []
    for index in range(target_questions):
        item = bank[index % len(bank)]
        section_id = sections[index % len(sections)].get("section_id") if sections else None
        questions.append(_bank_to_question(item, f"exam-{index + 1}", section_id))
    return questions, "mock"


def grade_lab(
    section_title: str,
    instructions: str | None,
    solution_summary: str,
    rubric: list[dict] | None,
) -> dict:
    """Califica un lab por rubrica. Devuelve {score, passed, feedback, criteria, source_mode}."""
    rubric = rubric or [
        {"criterion": "Funcionalidad", "weight": 40},
        {"criterion": "Claridad", "weight": 30},
        {"criterion": "Buenas practicas", "weight": 30},
    ]
    prompt = (
        f"Evalua la solucion de un laboratorio de la seccion «{section_title}».\n"
        f"Instrucciones: {instructions or 'N/D'}\n"
        f"Rubrica (criterios y peso): {rubric}\n"
        f"Solucion del alumno:\n{solution_summary}\n\n"
        'Devuelve SOLO JSON: {"score":0-100,"feedback":"...","criteria":{"<criterio>":<puntos>}}. '
        "Se justo y especifico; penaliza soluciones vacias o sin sustancia."
    )
    parsed = run_agent_json("gini-eval", prompt, temperature=0.2, max_tokens=700)
    if parsed and isinstance(parsed.get("score"), (int, float)):
        score = int(max(0, min(100, parsed["score"])))
        return {
            "score": score,
            "passed": score >= PASS_THRESHOLD,
            "feedback": str(parsed.get("feedback", "")),
            "criteria": parsed.get("criteria", {}),
            "source_mode": "foundry",
        }

    # Fallback heuristico: cobertura por longitud + senales de sustancia.
    text = (solution_summary or "").strip()
    length = len(text)
    has_signal = any(token in text.lower() for token in ("porque", "implement", "config", "paso", "ejemplo", "codigo", "code"))
    base = 35 if length < 60 else 60 if length < 160 else 78 if length < 320 else 88
    score = min(95, base + (7 if has_signal else 0))
    passed = score >= PASS_THRESHOLD
    return {
        "score": score,
        "passed": passed,
        "feedback": (
            "Solucion suficiente para aprobar; profundiza en justificaciones tecnicas."
            if passed
            else "La solucion es muy breve o poco sustentada. Explica que implementaste y por que."
        ),
        "criteria": {
            "functionality": min(40, max(15, score - 35)),
            "clarity": min(30, max(10, score - 45)),
            "best_practices": min(30, max(10, score - 40)),
        },
        "source_mode": "mock",
    }
