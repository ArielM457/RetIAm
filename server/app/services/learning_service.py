import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.db.supabase import get_supabase_service_client
from app.integrations.workiq_adapter import get_mock_calendar_context
from app.integrations.foundry_adapter import foundry_enabled
from app.models.certification import (
    CertificationRouteResponse,
    ResourceReference,
    RouteProfileContext,
    RouteSection,
)
from app.models.learning import (
    AgendaItemResponse,
    CourseEnrollmentResponse,
    EnrollmentFlowResponse,
    EnrollCourseRequest,
    GeneratePlanRequest,
    GenerateRouteRequest,
    PlanCheckin,
    StudySessionPlan,
    StudyPlanResponse,
    TeamCertificationAssignmentRequest,
    TeamCertificationAssignmentResponse,
    WeeklyMilestone,
)
from app.services._shared import response_data
from app.services.course_service import get_course_detail
from app.services.onboarding_catalog import CERTIFICATION_TRACK_HINTS
from app.services.profile_service import ensure_profile_for_user
from app.core.config import get_settings
from app.services.team_service import _ensure_manager_access

logger = logging.getLogger(__name__)

DAY_INDEX = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


ROUTE_TEMPLATES = {
    "azure": [
        {
            "section_id": "sec-az-foundations",
            "title": "Fundamentos del ecosistema Azure",
            "estimated_hours": 3,
            "resources": [
                {
                    "title": "Azure fundamentals synthetic guide",
                    "type": "documentation",
                    "source": "az-fundamentals-synthetic.md",
                    "url": "https://learn.microsoft.com/azure",
                }
            ],
        },
        {
            "section_id": "sec-az-services",
            "title": "Servicios core y seguridad",
            "estimated_hours": 4,
            "resources": [
                {
                    "title": "Core services and security",
                    "type": "documentation",
                    "source": "az-core-services-synthetic.md",
                    "url": "https://learn.microsoft.com/azure/architecture/",
                }
            ],
        },
        {
            "section_id": "sec-az-practice",
            "title": "Practica guiada y escenarios",
            "estimated_hours": 5,
            "resources": [
                {
                    "title": "Azure practice lab",
                    "type": "lab",
                    "source": "az-practice-lab-synthetic.md",
                    "url": "https://learn.microsoft.com/training/azure/",
                }
            ],
        },
    ],
    "aws": [
        {
            "section_id": "sec-aws-foundations",
            "title": "Fundamentos de AWS",
            "estimated_hours": 3,
            "resources": [
                {
                    "title": "AWS synthetic fundamentals",
                    "type": "documentation",
                    "source": "aws-fundamentals-synthetic.md",
                    "url": "https://docs.aws.amazon.com/",
                }
            ],
        },
        {
            "section_id": "sec-aws-architecture",
            "title": "Arquitectura, storage e integracion",
            "estimated_hours": 4,
            "resources": [
                {
                    "title": "AWS architecture notes",
                    "type": "documentation",
                    "source": "aws-architecture-synthetic.md",
                    "url": "https://docs.aws.amazon.com/wellarchitected/",
                }
            ],
        },
        {
            "section_id": "sec-aws-practice",
            "title": "Practica de escenarios cloud",
            "estimated_hours": 4,
            "resources": [
                {
                    "title": "AWS scenario lab",
                    "type": "lab",
                    "source": "aws-scenarios-synthetic.md",
                    "url": "https://skillbuilder.aws/",
                }
            ],
        },
    ],
    "github": [
        {
            "section_id": "sec-gh-collab",
            "title": "Colaboracion y flujo con pull requests",
            "estimated_hours": 2,
            "resources": [
                {
                    "title": "GitHub collaboration guide",
                    "type": "documentation",
                    "source": "github-collaboration-synthetic.md",
                    "url": "https://docs.github.com/",
                }
            ],
        },
        {
            "section_id": "sec-gh-actions",
            "title": "Automatizacion con GitHub Actions",
            "estimated_hours": 3,
            "resources": [
                {
                    "title": "GitHub Actions playbook",
                    "type": "documentation",
                    "source": "github-actions-synthetic.md",
                    "url": "https://docs.github.com/actions",
                }
            ],
        },
        {
            "section_id": "sec-gh-security",
            "title": "Seguridad y buenas practicas",
            "estimated_hours": 3,
            "resources": [
                {
                    "title": "GitHub security baseline",
                    "type": "documentation",
                    "source": "github-security-synthetic.md",
                    "url": "https://docs.github.com/code-security",
                }
            ],
        },
    ],
}


def _resolve_track(certification: str) -> str:
    if certification in CERTIFICATION_TRACK_HINTS:
        return CERTIFICATION_TRACK_HINTS[certification]
    normalized = certification.lower()
    if "aws" in normalized:
        return "aws"
    if "github" in normalized:
        return "github"
    return "azure"


def _get_profile_data(user_id: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=404, detail="Perfil no encontrado.")
    return data[0]


def _get_course_row(certification_code: str) -> dict:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_courses_table)
        .select("*")
        .eq("certification_code", certification_code)
        .limit(1)
        .execute()
    )
    data = response_data(response, [])
    if not data:
        raise HTTPException(status_code=404, detail="Curso no encontrado en el catalogo.")
    return data[0]


def _get_latest_assessment(user_id: str, target_certification: str | None = None) -> dict | None:
    settings = get_settings()
    query = (
        get_supabase_service_client()
        .table(settings.supabase_profile_assessments_table)
        .select("*")
        .eq("user_id", user_id)
    )
    if target_certification:
        query = query.eq("target_certification", target_certification)
    response = query.order("created_at", desc=True).limit(1).execute()
    data = response_data(response, [])
    return data[0] if data else None


def _normalize_preference_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    if isinstance(raw, str):
        return [item.strip() for item in raw.split(",") if item.strip()]
    return []


def _extract_assessment_preferences(assessment: dict | None) -> dict[str, list[str]]:
    answers = assessment.get("answers") if isinstance(assessment, dict) else []
    extracted: dict[str, list[str]] = {
        "content_preferences": [],
        "study_techniques": [],
        "learning_goals": [],
        "technology_experience": [],
    }
    if not isinstance(answers, list):
        return extracted

    for answer in answers:
        if not isinstance(answer, dict):
            continue
        key = str(answer.get("key") or answer.get("question_id") or "").strip().lower()
        title = str(answer.get("title") or "").strip().lower()
        value = str(answer.get("answer") or answer.get("selected_option_key") or "").strip()
        if not value:
            continue
        bucket = None
        if key in extracted:
            bucket = key
        elif "goal" in key or "objetivo" in title:
            bucket = "learning_goals"
        elif "content" in key or "contenido" in title:
            bucket = "content_preferences"
        elif "technique" in key or "tecnica" in title:
            bucket = "study_techniques"
        elif "experience" in key or "tecnolog" in title:
            bucket = "technology_experience"
        if bucket:
            extracted[bucket].extend(_normalize_preference_list(value))
    return {name: list(dict.fromkeys(values)) for name, values in extracted.items()}


def _normalize_study_days(raw: object) -> list[str]:
    if isinstance(raw, list):
        days = [str(item).strip() for item in raw if str(item).strip()]
    elif isinstance(raw, str):
        days = [item.strip() for item in raw.split(",") if item.strip()]
    else:
        days = []
    return [day for day in days if day in DAY_INDEX]


def _resolve_session_duration_minutes(
    weekly_hours: int,
    learning_style: list[str],
    study_techniques: list[str],
    preferred_study_days: list[str],
) -> int:
    if "pomodoro" in [item.lower() for item in study_techniques]:
        return 30
    day_count = max(1, len(preferred_study_days) or 1)
    distributed = max(30, round((weekly_hours * 60) / day_count / 5) * 5)
    if "hands_on" in learning_style:
        return min(90, max(60, distributed))
    if weekly_hours <= 4:
        return min(60, distributed)
    if weekly_hours >= 10:
        return min(90, max(60, distributed))
    return min(90, max(45, distributed))


def _build_profile_context(
    user_id: str,
    profile_data: dict,
    target_certification: str,
) -> RouteProfileContext:
    assessment = _get_latest_assessment(user_id, target_certification) or _get_latest_assessment(user_id) or {}
    extracted = _extract_assessment_preferences(assessment)
    weekly_hours = int(profile_data.get("weekly_hours_available") or assessment.get("weekly_hours_available") or 4)
    preferred_time = str(profile_data.get("preferred_time") or assessment.get("preferred_time") or "morning")
    preferred_start_hour = profile_data.get("preferred_start_hour")
    if preferred_start_hour is None and assessment:
        preferred_start_hour = assessment.get("preferred_start_hour")
    learning_style = _normalize_preference_list(
        profile_data.get("learning_style") or (assessment or {}).get("learning_style") or []
    )
    preferred_study_days = _normalize_study_days(
        profile_data.get("preferred_study_days") or (assessment or {}).get("preferred_study_days") or []
    )
    content_preferences = _normalize_preference_list(
        profile_data.get("content_preferences") or extracted["content_preferences"]
    )
    study_techniques = _normalize_preference_list(
        profile_data.get("study_techniques") or extracted["study_techniques"]
    )
    learning_goals = _normalize_preference_list(
        profile_data.get("learning_goals") or extracted["learning_goals"]
    )
    technology_experience = _normalize_preference_list(
        profile_data.get("technology_experience") or extracted["technology_experience"]
    )
    workiq_context = get_mock_calendar_context(
        preferred_time,
        weekly_hours,
        int(preferred_start_hour) if preferred_start_hour is not None else None,
        preferred_study_days,
    )
    recommended_days = _normalize_study_days(workiq_context.get("recommended_study_days") or preferred_study_days)
    session_duration = _resolve_session_duration_minutes(
        weekly_hours,
        learning_style,
        study_techniques,
        recommended_days,
    )
    return RouteProfileContext(
        weekly_hours_available=weekly_hours,
        preferred_time=preferred_time,
        preferred_start_hour=int(preferred_start_hour) if preferred_start_hour is not None else None,
        preferred_study_days=preferred_study_days,
        learning_style=learning_style,
        content_preferences=content_preferences,
        study_techniques=study_techniques,
        learning_goals=learning_goals,
        technology_experience=technology_experience,
        recommended_study_days=recommended_days,
        recommended_session_duration_minutes=session_duration,
        weekly_study_minutes=max(60, weekly_hours * 60),
    )


def _base_methodologies_for_profile(profile_context: RouteProfileContext, detected_level: str) -> list[str]:
    methods: list[str] = []
    style = {item.lower() for item in profile_context.learning_style}
    preferences = {item.lower() for item in profile_context.content_preferences}
    techniques = {item.lower() for item in profile_context.study_techniques}

    if "hands_on" in style or "practica" in preferences:
        methods.append("Practica guiada con checkpoints")
    if "code_examples" in style or "codigo" in preferences:
        methods.append("Repaso con ejemplos de codigo")
    if "documentation" in style or "textos" in preferences:
        methods.append("Lectura activa con notas cortas")
    if "mixed" in style or not methods:
        methods.append("Bloques mixtos de teoria y practica")
    if "pomodoro" in techniques:
        methods.append("Pomodoro con descansos cortos")
    if detected_level == "basic":
        methods.append("Micro sesiones de refuerzo")
    elif detected_level == "advanced":
        methods.append("Validacion rapida con retos")
    return list(dict.fromkeys(methods))


def _build_personalization_summary(
    profile_context: RouteProfileContext,
    detected_level: str,
) -> list[str]:
    style_text = ", ".join(profile_context.learning_style) if profile_context.learning_style else "mixto"
    summary = [
        (
            f"Plan adaptado para {profile_context.weekly_hours_available} horas semanales "
            f"en horario {profile_context.preferred_time}."
        ),
        f"Nivel detectado: {detected_level}.",
        f"Metodologia dominante: {style_text}.",
    ]
    if profile_context.preferred_start_hour is not None:
        summary.append(
            f"Sesiones ancladas desde las {profile_context.preferred_start_hour:02d}:00."
        )
    if profile_context.preferred_study_days:
        summary.append(
            "Dias preferidos: " + ", ".join(profile_context.preferred_study_days) + "."
        )
    if profile_context.study_techniques:
        summary.append(
            "Tecnicas integradas: " + ", ".join(profile_context.study_techniques[:3]) + "."
        )
    if profile_context.learning_goals:
        summary.append(
            "Objetivos priorizados: " + ", ".join(profile_context.learning_goals[:2]) + "."
        )
    return summary


def _build_route_sections_from_template(track: str) -> list[RouteSection]:
    sections: list[RouteSection] = []
    for index, section in enumerate(ROUTE_TEMPLATES[track], start=1):
        sections.append(
            RouteSection(
                section_id=section["section_id"],
                title=section["title"],
                order=index,
                estimated_hours=section["estimated_hours"],
                resources=[ResourceReference.model_validate(item) for item in section["resources"]],
                prerequisite_sections=[] if index == 1 else [ROUTE_TEMPLATES[track][index - 2]["section_id"]],
            )
        )
    return sections


def _build_route_sections_from_course(target_certification: str) -> list[RouteSection] | None:
    """Construye secciones desde el catalogo real (MS Learn ingerido). None si no hay curso."""
    course = get_course_detail(target_certification)
    if not course or not course.sections:
        return None
    sections: list[RouteSection] = []
    previous_key: str | None = None
    for index, section in enumerate(course.sections, start=1):
        estimated_hours = max(1, round((section.duration_minutes or 0) / 60))
        resources = [
            ResourceReference(
                title=source.title,
                type="documentation",
                source=source.source or "ms_learn",
                url=source.url or "https://learn.microsoft.com/training/",
            )
            for lesson in section.lessons
            for source in lesson.sources
        ][:4]
        sections.append(
            RouteSection(
                section_id=section.section_key,
                title=section.title,
                order=index,
                estimated_hours=estimated_hours,
                resources=resources,
                prerequisite_sections=[] if previous_key is None else [previous_key],
                duration_minutes=section.duration_minutes or 0,
                course_section_id=section.id,
                lessons=section.lessons,
                labs=section.labs,
            )
        )
        previous_key = section.section_key
    return sections


def _build_route_sections(track: str, target_certification: str) -> list[RouteSection]:
    """Prefiere el catalogo de cursos real; cae a la plantilla legacy si no existe."""
    from_course = _build_route_sections_from_course(target_certification)
    if from_course:
        return from_course
    logger.info("Sin curso en catalogo para %s; uso plantilla legacy del track %s", target_certification, track)
    return _build_route_sections_from_template(track)


def _section_session_type(section: RouteSection, learning_style: list[str]) -> str:
    styles = {item.lower() for item in learning_style}
    if section.labs and ("hands_on" in styles or "mixed" in styles):
        return "practice"
    if "code_examples" in styles:
        return "practice"
    return "theory"


def _section_methods(
    section: RouteSection,
    base_methods: list[str],
    profile_context: RouteProfileContext,
) -> list[str]:
    methods = list(base_methods)
    if section.labs:
        methods.append("Aplicacion inmediata en laboratorio")
    if section.lessons and any(lesson.learning_objectives for lesson in section.lessons):
        methods.append("Cierre con autoexplicacion de objetivos")
    if profile_context.content_preferences:
        methods.append(
            "Contenido presentado segun preferencias: "
            + ", ".join(profile_context.content_preferences[:2])
        )
    return list(dict.fromkeys(methods))


def _section_review_points(section: RouteSection, detected_level: str) -> list[str]:
    review_points: list[str] = []
    if section.lessons:
        first_lesson = section.lessons[0]
        review_points.append(f"Verificar comprension de {first_lesson.title}.")
    if section.labs:
        review_points.append("Completar laboratorio o simulacion clave de la seccion.")
    if detected_level == "basic":
        review_points.append("Hacer recap de conceptos antes de avanzar.")
    else:
        review_points.append("Responder preguntas de aplicacion antes de desbloquear la siguiente seccion.")
    return review_points


def _personalize_route_sections(
    sections: list[RouteSection],
    profile_context: RouteProfileContext,
    detected_level: str,
) -> list[RouteSection]:
    base_methods = _base_methodologies_for_profile(profile_context, detected_level)
    personalized: list[RouteSection] = []
    for index, section in enumerate(sections):
        unlock_after = sections[index - 1].section_id if index > 0 else None
        personalized.append(
            section.model_copy(
                update={
                    "recommended_session_type": _section_session_type(
                        section,
                        profile_context.learning_style,
                    ),
                    "recommended_study_methods": _section_methods(
                        section,
                        base_methods,
                        profile_context,
                    ),
                    "target_lessons": len(section.lessons),
                    "target_labs": len(section.labs),
                    "review_points": _section_review_points(section, detected_level),
                    "unlock_after_section_id": unlock_after,
                }
            )
        )
    return personalized


def _create_route_for_user(user_id: str, target_certification: str, detected_level: str) -> CertificationRouteResponse:
    settings = get_settings()
    profile_data = _get_profile_data(user_id)
    track = _resolve_track(target_certification)
    profile_context = _build_profile_context(user_id, profile_data, target_certification)
    sections = _personalize_route_sections(
        _build_route_sections(track, target_certification),
        profile_context,
        detected_level,
    )
    personalization_summary = _build_personalization_summary(profile_context, detected_level)
    has_real_content = any(section.lessons for section in sections)
    source_mode = "foundry" if (foundry_enabled() or has_real_content) else "mock"
    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_routes_table)
        .insert(
            {
                "user_id": user_id,
                "target_certification": target_certification,
                "detected_level": detected_level or "basic",
                "sections": [section.model_dump() for section in sections],
                "source_mode": source_mode,
                "profile_context": profile_context.model_dump(),
                "personalization_summary": personalization_summary,
            }
        )
        .execute()
    )
    route_data = response_data(response, [])[0]
    return CertificationRouteResponse(
        id=route_data["id"],
        target_certification=route_data["target_certification"],
        detected_level=route_data["detected_level"],
        source_mode=route_data["source_mode"],
        sections=sections,
        personalization_summary=route_data.get("personalization_summary") or personalization_summary,
        profile_context=RouteProfileContext.model_validate(
            route_data.get("profile_context") or profile_context.model_dump()
        ),
    )


def _pick_focus_points(section: RouteSection, lesson_ids: list[str]) -> list[str]:
    focus_points: list[str] = []
    lesson_id_set = set(lesson_ids)
    for lesson in section.lessons:
        if lesson.id in lesson_id_set:
            focus_points.extend(lesson.learning_objectives[:2])
    if not focus_points and section.review_points:
        focus_points.extend(section.review_points[:2])
    if not focus_points:
        focus_points.append(f"Dominar los puntos clave de {section.title}.")
    return list(dict.fromkeys(focus_points))[:3]


def _build_section_sessions(
    section: RouteSection,
    session_duration_minutes: int,
    recommended_days: list[str],
    preferred_windows: list[str],
) -> list[StudySessionPlan]:
    sessions: list[StudySessionPlan] = []
    lessons = section.lessons or []
    day_count = max(1, len(recommended_days) or 1)
    window_count = max(1, len(preferred_windows) or 1)
    lesson_pointer = 0
    session_index = 1

    if lessons:
        current_ids: list[str] = []
        current_titles: list[str] = []
        current_minutes = 0
        while lesson_pointer < len(lessons):
            lesson = lessons[lesson_pointer]
            lesson_minutes = max(15, int(lesson.duration_minutes or 20))
            if current_ids and current_minutes + lesson_minutes > session_duration_minutes + 15:
                slot_index = len(sessions)
                sessions.append(
                    StudySessionPlan(
                        session_id=f"{section.section_id}-session-{session_index}",
                        title=f"{section.title} · Bloque {session_index}",
                        session_type=section.recommended_session_type,
                        day_name=(recommended_days or ["Monday"])[slot_index % day_count],
                        time_window=(preferred_windows or ["08:00-09:00"])[slot_index % window_count],
                        duration_minutes=max(session_duration_minutes, current_minutes),
                        section_id=section.section_id,
                        lesson_ids=current_ids,
                        methodologies=section.recommended_study_methods,
                        focus_points=_pick_focus_points(section, current_ids),
                    )
                )
                session_index += 1
                current_ids = []
                current_titles = []
                current_minutes = 0
                continue
            if lesson.id:
                current_ids.append(lesson.id)
            current_titles.append(lesson.title)
            current_minutes += lesson_minutes
            lesson_pointer += 1

        if current_ids:
            slot_index = len(sessions)
            sessions.append(
                StudySessionPlan(
                    session_id=f"{section.section_id}-session-{session_index}",
                    title=f"{section.title} · Bloque {session_index}",
                    session_type=section.recommended_session_type,
                    day_name=(recommended_days or ["Monday"])[slot_index % day_count],
                    time_window=(preferred_windows or ["08:00-09:00"])[slot_index % window_count],
                    duration_minutes=max(session_duration_minutes, current_minutes),
                    section_id=section.section_id,
                    lesson_ids=current_ids,
                    methodologies=section.recommended_study_methods,
                    focus_points=_pick_focus_points(section, current_ids),
                )
            )
            session_index += 1
    else:
        sessions.append(
            StudySessionPlan(
                session_id=f"{section.section_id}-session-{session_index}",
                title=f"{section.title} · Exploracion guiada",
                session_type=section.recommended_session_type,
                day_name=(recommended_days or ["Monday"])[0],
                time_window=(preferred_windows or ["08:00-09:00"])[0],
                duration_minutes=session_duration_minutes,
                section_id=section.section_id,
                methodologies=section.recommended_study_methods,
                focus_points=section.review_points[:2] or [f"Revisar fundamentos de {section.title}."],
            )
        )
        session_index += 1

    for lab in section.labs:
        slot_index = len(sessions)
        sessions.append(
            StudySessionPlan(
                session_id=f"{section.section_id}-lab-{session_index}",
                title=f"{section.title} · Lab {lab.title}",
                session_type="lab",
                day_name=(recommended_days or ["Monday"])[slot_index % day_count],
                time_window=(preferred_windows or ["08:00-09:00"])[slot_index % window_count],
                duration_minutes=max(session_duration_minutes, int(lab.estimated_minutes or 45)),
                section_id=section.section_id,
                methodologies=section.recommended_study_methods,
                focus_points=[lab.title, "Aplicar lo aprendido en un escenario realista."],
            )
        )
        session_index += 1

    slot_index = len(sessions)
    sessions.append(
        StudySessionPlan(
            session_id=f"{section.section_id}-review-{session_index}",
            title=f"{section.title} · Revision y desbloqueo",
            session_type="review",
            day_name=(recommended_days or ["Monday"])[slot_index % day_count],
            time_window=(preferred_windows or ["08:00-09:00"])[slot_index % window_count],
            duration_minutes=max(30, session_duration_minutes // 2),
            section_id=section.section_id,
            methodologies=section.recommended_study_methods,
            focus_points=section.review_points[:3],
            is_review=True,
            unlocks=[section.section_id],
        )
    )
    return sessions


def _build_checkins(section_ids: list[str], week: int) -> list[PlanCheckin]:
    ids_text = ", ".join(section_ids)
    return [
        PlanCheckin(
            kind="weekly_review",
            title=f"Revision de avance semana {week}",
            trigger="end_of_week",
            success_criteria=[
                f"Completar las sesiones de {ids_text}.",
                "Registrar dudas y pedir apoyo al tutor si hay brechas.",
            ],
            recovery_action="Si no cumples el hito, mueve la siguiente revision al primer bloque libre y reduce el ritmo de la semana siguiente.",
        )
    ]


def _milestone_methodologies(
    sections: list[RouteSection],
    section_ids: list[str],
) -> list[str]:
    notes: list[str] = []
    wanted = set(section_ids)
    for section in sections:
        if section.section_id in wanted:
            notes.extend(section.recommended_study_methods[:2])
    return list(dict.fromkeys(notes))[:4]


def _parse_window_start(preferred_window: str) -> tuple[int, int]:
    start = (preferred_window or "08:00-09:00").split("-")[0]
    hour, minute = [int(part) for part in start.split(":")]
    return hour, minute


def _next_datetime_for_day(base: datetime, day_name: str, preferred_window: str) -> datetime:
    target_day = DAY_INDEX.get(day_name, 0)
    hour, minute = _parse_window_start(preferred_window)
    delta = (target_day - base.weekday()) % 7
    candidate = (base + timedelta(days=delta)).replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )
    if candidate <= base:
        candidate += timedelta(days=7)
    return candidate


def _load_busy_ranges(user_id: str, base: datetime) -> list[tuple[datetime, datetime]]:
    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_agenda_items_table)
        .select("scheduled_start,scheduled_end,status")
        .eq("user_id", user_id)
        .in_("status", ["scheduled", "rescheduled"])
        .gte("scheduled_end", base.isoformat())
        .order("scheduled_start")
        .execute()
    )
    items = response_data(response, []) or []
    ranges: list[tuple[datetime, datetime]] = []
    for item in items:
        try:
            ranges.append(
                (
                    datetime.fromisoformat(item["scheduled_start"].replace("Z", "+00:00")),
                    datetime.fromisoformat(item["scheduled_end"].replace("Z", "+00:00")),
                )
            )
        except Exception:
            continue
    return ranges


def _has_conflict(candidate_start: datetime, candidate_end: datetime, busy_ranges: list[tuple[datetime, datetime]]) -> bool:
    return any(candidate_start < busy_end and candidate_end > busy_start for busy_start, busy_end in busy_ranges)


def _find_next_free_slot(
    cursor: datetime,
    duration_minutes: int,
    preferred_days: list[str],
    preferred_windows: list[str],
    busy_ranges: list[tuple[datetime, datetime]],
) -> tuple[datetime, datetime, str]:
    days = preferred_days or ["Monday", "Thursday", "Friday"]
    windows = preferred_windows or ["08:00-09:00"]
    search_base = cursor
    for _ in range(120):
        candidates: list[tuple[datetime, datetime, str]] = []
        for day_name in days:
            for window in windows:
                start = _next_datetime_for_day(search_base, day_name, window)
                end = start + timedelta(minutes=duration_minutes)
                candidates.append((start, end, window))
        candidates.sort(key=lambda item: item[0])
        for start, end, window in candidates:
            if not _has_conflict(start, end, busy_ranges):
                return start, end, window
        search_base = search_base + timedelta(days=7)
    fallback_start = cursor + timedelta(days=1)
    fallback_end = fallback_start + timedelta(minutes=duration_minutes)
    return fallback_start, fallback_end, windows[0]


def _build_agenda_items_for_plan(
    user_id: str,
    enrollment_id: str,
    route: CertificationRouteResponse,
    plan: StudyPlanResponse,
) -> list[AgendaItemResponse]:
    workiq_context = plan.workiq_context or {}
    preferred_days = workiq_context.get("recommended_study_days") or route.profile_context.recommended_study_days
    preferred_windows = workiq_context.get("preferred_delivery_windows") or ["08:00-09:00"]
    cursor = datetime.now(timezone.utc)
    busy_ranges = _load_busy_ranges(user_id, cursor)
    agenda_items: list[AgendaItemResponse] = []

    for milestone in plan.weekly_milestones:
        for session in milestone.sessions:
            start, end, window = _find_next_free_slot(
                cursor,
                session.duration_minutes,
                preferred_days,
                preferred_windows,
                busy_ranges,
            )
            item_type = "lab" if session.session_type == "lab" else "review" if session.is_review else "study_session"
            agenda_items.append(
                AgendaItemResponse(
                    enrollment_id=enrollment_id,
                    plan_id=plan.id,
                    route_id=route.id,
                    title=session.title,
                    item_type=item_type,
                    related_session_id=session.session_id,
                    related_section_id=session.section_id,
                    related_lesson_ids=session.lesson_ids,
                    scheduled_start=start.isoformat(),
                    scheduled_end=end.isoformat(),
                    time_window=window,
                    status="scheduled",
                    metadata={
                        "week": milestone.week,
                        "session_type": session.session_type,
                        "focus_points": session.focus_points,
                        "methodologies": session.methodologies,
                        "unlocks": session.unlocks,
                    },
                )
            )
            busy_ranges.append((start, end))
            cursor = start + timedelta(minutes=5)

        for checkin in milestone.checkins:
            start, end, window = _find_next_free_slot(
                cursor,
                20,
                preferred_days,
                preferred_windows,
                busy_ranges,
            )
            agenda_items.append(
                AgendaItemResponse(
                    enrollment_id=enrollment_id,
                    plan_id=plan.id,
                    route_id=route.id,
                    title=checkin.title,
                    item_type="checkin",
                    related_section_id=",".join(milestone.section_ids),
                    scheduled_start=start.isoformat(),
                    scheduled_end=end.isoformat(),
                    time_window=window,
                    status="scheduled",
                    metadata={
                        "week": milestone.week,
                        "trigger": checkin.trigger,
                        "success_criteria": checkin.success_criteria,
                        "recovery_action": checkin.recovery_action,
                    },
                )
            )
            busy_ranges.append((start, end))
            cursor = start + timedelta(minutes=5)

    return agenda_items


def _persist_agenda_items(user_id: str, items: list[AgendaItemResponse]) -> list[AgendaItemResponse]:
    settings = get_settings()
    persisted: list[AgendaItemResponse] = []
    for item in items:
        response = (
            get_supabase_service_client()
            .table(settings.supabase_learning_agenda_items_table)
            .insert(
                {
                    "user_id": user_id,
                    "enrollment_id": item.enrollment_id,
                    "plan_id": item.plan_id,
                    "route_id": item.route_id,
                    "title": item.title,
                    "item_type": item.item_type,
                    "related_session_id": item.related_session_id,
                    "related_section_id": item.related_section_id,
                    "related_lesson_ids": item.related_lesson_ids,
                    "scheduled_start": item.scheduled_start,
                    "scheduled_end": item.scheduled_end,
                    "time_window": item.time_window,
                    "status": item.status,
                    "metadata": item.metadata,
                }
            )
            .execute()
        )
        data = response_data(response, [])[0]
        persisted.append(
            AgendaItemResponse(
                id=data["id"],
                enrollment_id=data.get("enrollment_id"),
                plan_id=data.get("plan_id"),
                route_id=data.get("route_id"),
                title=data["title"],
                item_type=data["item_type"],
                related_session_id=data.get("related_session_id"),
                related_section_id=data.get("related_section_id"),
                related_lesson_ids=data.get("related_lesson_ids") or [],
                scheduled_start=data["scheduled_start"],
                scheduled_end=data["scheduled_end"],
                time_window=data.get("time_window"),
                status=data["status"],
                metadata=data.get("metadata") or {},
            )
        )
    return persisted


def _build_plan_payload(
    user_id: str,
    route_data: dict,
    profile_data: dict,
    weekly_hours: int | None,
    preferred_time: str | None,
    requested_deadline: str | None,
) -> StudyPlanResponse:
    settings = get_settings()
    weekly_hours = weekly_hours or profile_data.get("weekly_hours_available") or 4
    preferred_time = preferred_time or profile_data.get("preferred_time") or "morning"
    sections = [RouteSection.model_validate(item) for item in route_data["sections"]]
    route_profile_context = RouteProfileContext.model_validate(
        route_data.get("profile_context")
        or {
            "weekly_hours_available": weekly_hours,
            "preferred_time": preferred_time,
            "preferred_start_hour": profile_data.get("preferred_start_hour"),
            "preferred_study_days": profile_data.get("preferred_study_days") or [],
            "learning_style": profile_data.get("learning_style") or [],
        }
    )
    total_hours = sum(section.estimated_hours for section in sections)
    capacity = max(1, int(weekly_hours * 0.8))
    weeks_needed = max(1, (total_hours + capacity - 1) // capacity)
    deadline = (
        datetime.fromisoformat(requested_deadline.replace("Z", "+00:00"))
        if requested_deadline
        else datetime.now(timezone.utc) + timedelta(weeks=weeks_needed)
    )

    workiq_context = get_mock_calendar_context(
        preferred_time,
        weekly_hours,
        route_profile_context.preferred_start_hour,
        route_profile_context.preferred_study_days,
    )
    session_duration_minutes = route_profile_context.recommended_session_duration_minutes
    recommended_days = (
        route_profile_context.preferred_study_days
        or workiq_context.get("recommended_study_days")
        or ["Monday", "Thursday"]
    )
    preferred_windows = workiq_context.get("preferred_delivery_windows") or ["08:00-09:00"]
    all_sessions: list[StudySessionPlan] = []
    for section in sections:
        all_sessions.extend(
            _build_section_sessions(
                section,
                session_duration_minutes,
                recommended_days,
                preferred_windows,
            )
        )

    weekly_capacity_minutes = max(60, weekly_hours * 60)
    milestones: list[WeeklyMilestone] = []
    current_sessions: list[StudySessionPlan] = []
    current_section_ids: list[str] = []
    current_minutes = 0
    week = 1
    for session in all_sessions:
        if current_sessions and current_minutes + session.duration_minutes > weekly_capacity_minutes:
            milestones.append(
                WeeklyMilestone(
                    week=week,
                    title=f"Semana {week}",
                    section_ids=list(dict.fromkeys(current_section_ids)),
                    estimated_hours=max(1, round(current_minutes / 60)),
                    focus=f"Completar {len(current_sessions)} sesiones con progreso desbloqueable.",
                    methodology_notes=_milestone_methodologies(
                        sections,
                        list(dict.fromkeys(current_section_ids)),
                    ),
                    sessions=current_sessions,
                    checkins=_build_checkins(list(dict.fromkeys(current_section_ids)), week),
                )
            )
            week += 1
            current_sessions = []
            current_section_ids = []
            current_minutes = 0
        current_sessions.append(session)
        current_section_ids.append(session.section_id)
        current_minutes += session.duration_minutes
    if current_sessions:
        milestones.append(
            WeeklyMilestone(
                week=week,
                title=f"Semana {week}",
                section_ids=list(dict.fromkeys(current_section_ids)),
                estimated_hours=max(1, round(current_minutes / 60)),
                focus=f"Completar {len(current_sessions)} sesiones con cierre semanal.",
                methodology_notes=_milestone_methodologies(
                    sections,
                    list(dict.fromkeys(current_section_ids)),
                ),
                sessions=current_sessions,
                checkins=_build_checkins(list(dict.fromkeys(current_section_ids)), week),
            )
        )

    workiq_context.update(
        {
            "recommended_session_duration_minutes": session_duration_minutes,
            "preferred_start_hour": route_profile_context.preferred_start_hour,
            "preferred_study_days": recommended_days,
            "weekly_study_minutes": route_profile_context.weekly_study_minutes or weekly_hours * 60,
            "rescheduling_rules": [
                "Si una sesion no se completa, moverla al siguiente bloque libre del mismo tipo.",
                "Si se fallan dos checkpoints seguidos, insertar una revision antes de liberar la siguiente seccion.",
                "Priorizar sesiones cortas de recuperacion cuando el avance real quede debajo del hito semanal.",
            ],
            "progression_mode": "locked_by_review",
        }
    )
    personalization_summary = route_data.get("personalization_summary") or _build_personalization_summary(
        route_profile_context,
        route_data.get("detected_level") or profile_data.get("detected_level") or "basic",
    )
    response = (
        get_supabase_service_client()
        .table(settings.supabase_study_plans_table)
        .insert(
            {
                "user_id": user_id,
                "route_id": route_data["id"],
                "target_certification": route_data["target_certification"],
                "deadline_at": deadline.isoformat(),
                "weekly_hours": weekly_hours,
                "weekly_milestones": [item.model_dump() for item in milestones],
                "workiq_context": workiq_context,
                "status": "active",
                "personalization_summary": personalization_summary,
            }
        )
        .execute()
    )
    plan = response_data(response, [])[0]
    return StudyPlanResponse(
        id=plan["id"],
        route_id=plan["route_id"],
        target_certification=plan["target_certification"],
        deadline_at=plan["deadline_at"],
        weekly_hours=plan["weekly_hours"],
        weekly_milestones=milestones,
        workiq_context=plan["workiq_context"],
        status=plan["status"],
        personalization_summary=plan.get("personalization_summary") or personalization_summary,
    )


def generate_learning_route(auth_user: object, payload: GenerateRouteRequest) -> CertificationRouteResponse:
    profile = ensure_profile_for_user(auth_user)
    profile_data = _get_profile_data(profile.id)
    return _create_route_for_user(
        profile.id,
        payload.target_certification,
        profile_data.get("detected_level") or "basic",
    )


def get_my_latest_route(auth_user: object) -> CertificationRouteResponse | None:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    try:
        response = (
            get_supabase_service_client()
            .table(settings.supabase_learning_routes_table)
            .select("*")
            .eq("user_id", profile.id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        logger.warning("Latest route lookup failed for user %s: %s", profile.id, exc)
        return None
    data = response_data(response, [])
    if not data:
        return None
    route = data[0]
    try:
        return CertificationRouteResponse(
            id=route["id"],
            target_certification=route["target_certification"],
            detected_level=route["detected_level"],
            source_mode=route["source_mode"],
            sections=[RouteSection.model_validate(item) for item in route.get("sections") or []],
            personalization_summary=route.get("personalization_summary") or [],
            profile_context=RouteProfileContext.model_validate(route.get("profile_context") or {}),
        )
    except Exception as exc:
        logger.warning("Latest route payload invalid for user %s: %s", profile.id, exc)
        return None


def generate_study_plan(auth_user: object, payload: GeneratePlanRequest) -> StudyPlanResponse:
    profile = ensure_profile_for_user(auth_user)
    profile_data = _get_profile_data(profile.id)
    settings = get_settings()
    route_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_routes_table)
        .select("*")
        .eq("id", payload.route_id)
        .eq("user_id", profile.id)
        .limit(1)
        .execute()
    )
    route_data = (response_data(route_response, []) or [None])[0]
    if not route_data:
        raise HTTPException(status_code=404, detail="Ruta no encontrada para este usuario.")
    return _build_plan_payload(
        profile.id,
        route_data,
        profile_data,
        payload.weekly_hours,
        payload.preferred_time,
        payload.requested_deadline,
    )


def enroll_in_course(auth_user: object, payload: EnrollCourseRequest) -> EnrollmentFlowResponse:
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="La inscripcion requiere confirmacion explicita.")

    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    profile_data = _get_profile_data(profile.id)
    course_row = _get_course_row(payload.certification_code)

    route = _create_route_for_user(
        profile.id,
        payload.certification_code,
        profile_data.get("detected_level") or "basic",
    )
    plan = _build_plan_payload(
        profile.id,
        {
            "id": route.id,
            "target_certification": route.target_certification,
            "detected_level": route.detected_level,
            "sections": [section.model_dump() for section in route.sections],
            "profile_context": route.profile_context.model_dump(),
            "personalization_summary": route.personalization_summary,
        },
        profile_data,
        route.profile_context.weekly_hours_available,
        route.profile_context.preferred_time,
        None,
    )

    enrollment_response = (
        get_supabase_service_client()
        .table(settings.supabase_course_enrollments_table)
        .upsert(
            {
                "user_id": profile.id,
                "course_id": course_row["id"],
                "certification_code": payload.certification_code,
                "status": "active",
                "activated_route_id": route.id,
                "activated_plan_id": plan.id,
                "preferences_snapshot": route.profile_context.model_dump(),
                "personalization_summary": route.personalization_summary,
                "current_section_id": route.sections[0].section_id if route.sections else None,
                "current_session_id": plan.weekly_milestones[0].sessions[0].session_id
                if plan.weekly_milestones and plan.weekly_milestones[0].sessions
                else None,
            },
            on_conflict="user_id,certification_code",
        )
        .execute()
    )
    enrollment_data = response_data(enrollment_response, [])[0]

    old_agenda_response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_agenda_items_table)
        .delete()
        .eq("user_id", profile.id)
        .eq("enrollment_id", enrollment_data["id"])
        .execute()
    )
    _ = old_agenda_response

    agenda_seed = _build_agenda_items_for_plan(profile.id, enrollment_data["id"], route, plan)
    agenda = _persist_agenda_items(profile.id, agenda_seed)

    enrollment = CourseEnrollmentResponse(
        id=enrollment_data["id"],
        user_id=enrollment_data["user_id"],
        course_id=enrollment_data["course_id"],
        certification_code=enrollment_data["certification_code"],
        status=enrollment_data["status"],
        enrolled_at=enrollment_data.get("enrolled_at"),
        activated_route_id=enrollment_data.get("activated_route_id"),
        activated_plan_id=enrollment_data.get("activated_plan_id"),
        preferences_snapshot=enrollment_data.get("preferences_snapshot") or {},
        personalization_summary=enrollment_data.get("personalization_summary") or [],
        current_section_id=enrollment_data.get("current_section_id"),
        current_session_id=enrollment_data.get("current_session_id"),
    )
    return EnrollmentFlowResponse(
        enrollment=enrollment,
        route=route,
        plan=plan,
        agenda=agenda,
    )


def list_my_agenda(auth_user: object) -> list[AgendaItemResponse]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_learning_agenda_items_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("scheduled_start")
        .execute()
    )
    items = response_data(response, []) or []
    return [
        AgendaItemResponse(
            id=item["id"],
            enrollment_id=item.get("enrollment_id"),
            plan_id=item.get("plan_id"),
            route_id=item.get("route_id"),
            title=item["title"],
            item_type=item["item_type"],
            related_session_id=item.get("related_session_id"),
            related_section_id=item.get("related_section_id"),
            related_lesson_ids=item.get("related_lesson_ids") or [],
            scheduled_start=item["scheduled_start"],
            scheduled_end=item["scheduled_end"],
            time_window=item.get("time_window"),
            status=item["status"],
            metadata=item.get("metadata") or {},
        )
        for item in items
    ]


def list_my_enrollments(auth_user: object) -> list[CourseEnrollmentResponse]:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    response = (
        get_supabase_service_client()
        .table(settings.supabase_course_enrollments_table)
        .select("*")
        .eq("user_id", profile.id)
        .order("enrolled_at", desc=True)
        .execute()
    )
    rows = response_data(response, []) or []
    return [
        CourseEnrollmentResponse(
            id=row.get("id"),
            user_id=row["user_id"],
            course_id=row["course_id"],
            certification_code=row["certification_code"],
            status=row.get("status") or "enrolled",
            enrolled_at=row.get("enrolled_at"),
            activated_route_id=row.get("activated_route_id"),
            activated_plan_id=row.get("activated_plan_id"),
            preferences_snapshot=row.get("preferences_snapshot") or {},
            personalization_summary=row.get("personalization_summary") or [],
            current_section_id=row.get("current_section_id"),
            current_session_id=row.get("current_session_id"),
        )
        for row in rows
    ]


def get_my_latest_plan(auth_user: object) -> StudyPlanResponse | None:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    try:
        response = (
            get_supabase_service_client()
            .table(settings.supabase_study_plans_table)
            .select("*")
            .eq("user_id", profile.id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        logger.warning("Latest plan lookup failed for user %s: %s", profile.id, exc)
        return None
    data = response_data(response, [])
    if not data:
        return None
    plan = data[0]
    try:
        return StudyPlanResponse(
            id=plan["id"],
            route_id=plan["route_id"],
            target_certification=plan["target_certification"],
            deadline_at=plan["deadline_at"],
            weekly_hours=plan["weekly_hours"],
            weekly_milestones=[
                WeeklyMilestone.model_validate(item) for item in (plan.get("weekly_milestones") or [])
            ],
            workiq_context=plan.get("workiq_context") or {},
            status=plan["status"],
            personalization_summary=plan.get("personalization_summary") or [],
        )
    except Exception as exc:
        logger.warning("Latest plan payload invalid for user %s: %s", profile.id, exc)
        return None


def assign_certification_to_team(
    auth_user: object,
    team_id: str,
    payload: TeamCertificationAssignmentRequest,
) -> TeamCertificationAssignmentResponse:
    settings = get_settings()
    profile = ensure_profile_for_user(auth_user)
    _ensure_manager_access(team_id, profile.id)
    team_members_response = (
        get_supabase_service_client()
        .table(settings.supabase_team_members_table)
        .select("user_id")
        .eq("team_id", team_id)
        .execute()
    )
    valid_member_ids = {item["user_id"] for item in (response_data(team_members_response, []) or [])}
    invalid_members = [member_id for member_id in payload.member_ids if member_id not in valid_member_ids]
    if invalid_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Los siguientes usuarios no pertenecen al equipo: {', '.join(invalid_members)}",
        )

    response = (
        get_supabase_service_client()
        .table(settings.supabase_team_cert_assignments_table)
        .insert(
            {
                "team_id": team_id,
                "assigned_by": profile.id,
                "target_certification": payload.target_certification,
                "member_ids": payload.member_ids,
            }
        )
        .execute()
    )
    data = response_data(response, [])[0]
    generated_plan_count = 0
    notifications_created = 0
    for member_id in payload.member_ids:
        member_profile = _get_profile_data(member_id)
        route = _create_route_for_user(
            member_id,
            payload.target_certification,
            member_profile.get("detected_level") or "basic",
        )
        route_data = {
            "id": route.id,
            "target_certification": route.target_certification,
            "sections": [section.model_dump() for section in route.sections],
        }
        _build_plan_payload(
            member_id,
            route_data,
            member_profile,
            member_profile.get("weekly_hours_available"),
            member_profile.get("preferred_time"),
            None,
        )
        generated_plan_count += 1
        get_supabase_service_client().table(settings.supabase_profiles_table).update(
            {"target_certification": payload.target_certification}
        ).eq("id", member_id).execute()
        get_supabase_service_client().table(settings.supabase_coach_reminders_table).insert(
            {
                "user_id": member_id,
                "plan_id": None,
                "kind": "standard",
                "tone": "formal",
                "delivery_channel": "platform",
                "message": (
                    f"Tu manager te asigno la certificacion {payload.target_certification}. "
                    "Ya dejamos tu ruta y plan inicial listos."
                ),
                "scheduled_for": datetime.now(timezone.utc).isoformat(),
                "status": "scheduled",
            }
        ).execute()
        notifications_created += 1
    return TeamCertificationAssignmentResponse(
        id=data["id"],
        team_id=data["team_id"],
        target_certification=data["target_certification"],
        member_ids=data["member_ids"],
        generated_plan_count=generated_plan_count,
        notifications_created=notifications_created,
        created_at=data["created_at"],
    )
