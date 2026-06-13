"""Ranking del equipo con apoyo de un agente.

Cruza datos reales (sesiones de aprendizaje, tiempos, aprobacion de examenes,
progreso y estilo de aprendizaje) para producir:
- un ranking de miembros (top performers),
- el "record de tiempo" (quien completa mas rapido),
- la "mejor metodologia" (que estilo de aprendizaje rinde mejor en el equipo),
- un texto de insight redactado por el agente (gpt-4o), con degradacion si no hay IA.
"""

import logging
from datetime import datetime

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import run_agent
from app.services._shared import response_data
from app.services.manager_service import _member_progress
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import _ensure_manager_access

logger = logging.getLogger(__name__)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _member_stats(member_id: str) -> dict:
    settings = get_settings()
    client = get_supabase_service_client()

    sessions = response_data(
        client.table(settings.supabase_learning_sessions_table)
        .select("status,started_at,completed_at")
        .eq("user_id", member_id)
        .execute(),
        [],
    ) or []
    completed = [s for s in sessions if s.get("status") == "completed"]
    durations: list[float] = []
    for s in completed:
        start = _parse_dt(s.get("started_at"))
        end = _parse_dt(s.get("completed_at"))
        if start and end and end > start:
            durations.append((end - start).total_seconds() / 60.0)

    exams = response_data(
        client.table(settings.supabase_exam_attempts_table)
        .select("passed,submitted_at")
        .eq("user_id", member_id)
        .execute(),
        [],
    ) or []
    submitted = [e for e in exams if e.get("submitted_at")]
    passed = len([e for e in submitted if e.get("passed")])
    pass_rate = round((passed / len(submitted)) * 100) if submitted else 0

    progress, _, _ = _member_progress(member_id)

    return {
        "completed_sessions": len(completed),
        "study_minutes": round(sum(durations)),
        "fastest_minutes": round(min(durations)) if durations else None,
        "avg_minutes": round(sum(durations) / len(durations)) if durations else None,
        "exams_taken": len(submitted),
        "exams_passed": passed,
        "pass_rate": pass_rate,
        "progress_percent": progress,
    }


def _score(stats: dict) -> float:
    # Score compuesto simple para ordenar el ranking.
    return (
        stats["progress_percent"] * 0.5
        + stats["pass_rate"] * 0.3
        + stats["completed_sessions"] * 4
    )


def get_team_ranking(auth_user: object, team_id: str) -> dict:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    team = _ensure_manager_access(team_id, profile.id)
    client = get_supabase_service_client()

    member_rows = response_data(
        client.table(settings.supabase_team_members_table)
        .select("user_id")
        .eq("team_id", team_id)
        .execute(),
        [],
    ) or []

    members: list[dict] = []
    style_buckets: dict[str, list[int]] = {}
    for row in member_rows:
        member_id = row["user_id"]
        prof = response_data(
            client.table(settings.supabase_profiles_table)
            .select("id,full_name,learning_style")
            .eq("id", member_id)
            .limit(1)
            .execute(),
            [],
        )
        prof = (prof or [None])[0]
        if not prof:
            continue
        stats = _member_stats(member_id)
        styles = prof.get("learning_style") or []
        entry = {
            "user_id": member_id,
            "full_name": prof.get("full_name") or "Miembro",
            "learning_style": styles,
            "score": round(_score(stats), 1),
            **stats,
        }
        members.append(entry)
        for style in styles:
            style_buckets.setdefault(str(style), []).append(stats["progress_percent"])

    members.sort(key=lambda m: m["score"], reverse=True)
    for index, member in enumerate(members, start=1):
        member["rank"] = index

    # Record de tiempo: completa una seccion mas rapido (minutos > 0).
    timed = [m for m in members if m.get("fastest_minutes")]
    record_holder = min(timed, key=lambda m: m["fastest_minutes"]) if timed else None

    # Mejor metodologia: estilo de aprendizaje con mejor progreso promedio.
    methodology = [
        {"style": style, "avg_progress": round(sum(vals) / len(vals)), "members": len(vals)}
        for style, vals in style_buckets.items()
        if vals
    ]
    methodology.sort(key=lambda m: m["avg_progress"], reverse=True)
    best_methodology = methodology[0] if methodology else None

    narrative = _build_narrative(team.get("name"), members, record_holder, methodology)

    return {
        "team_id": team_id,
        "team_name": team.get("name"),
        "members": members,
        "record_holder": record_holder,
        "best_methodology": best_methodology,
        "methodology_breakdown": methodology,
        "narrative": narrative,
    }


def _build_narrative(
    team_name: str | None,
    members: list[dict],
    record_holder: dict | None,
    methodology: list[dict],
) -> str:
    if not members:
        return "Aun no hay datos suficientes del equipo para generar un ranking."

    top = members[0]
    facts = [
        f"Equipo: {team_name or 'sin nombre'}.",
        f"Top performer: {top['full_name']} (score {top['score']}, "
        f"progreso {top['progress_percent']}%, {top['completed_sessions']} sesiones).",
    ]
    if record_holder:
        facts.append(
            f"Record de tiempo: {record_holder['full_name']} completo una seccion en "
            f"{record_holder['fastest_minutes']} min."
        )
    if methodology:
        facts.append(
            "Metodologias por progreso promedio: "
            + ", ".join(f"{m['style']} ({m['avg_progress']}%)" for m in methodology[:3])
            + "."
        )

    prompt = (
        "Eres un agente analista de aprendizaje. Con estos DATOS de un equipo, escribe un "
        "insight BREVE (3 a 4 frases, en espanol, tono ejecutivo y motivador) que destaque al "
        "mejor desempeno, el record de tiempo y RECOMIENDE la mejor metodologia de ensenanza "
        "para el equipo. No inventes datos.\n\nDATOS:\n- " + "\n- ".join(facts)
    )
    result = run_agent("team-analyst", prompt, temperature=0.4, max_tokens=300, ground=False)
    if result and result.get("text"):
        return result["text"].strip()
    # Fallback sin IA: resumen plano con los hechos calculados.
    extra = ""
    if methodology:
        extra = f" La metodologia con mejor progreso es {methodology[0]['style']}."
    return " ".join(facts) + extra
