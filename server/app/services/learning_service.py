import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.db.supabase import get_supabase_service_client
from app.integrations.foundry_adapter import foundry_enabled
from app.integrations.workiq_adapter import get_mock_calendar_context
from app.models.certification import CertificationRouteResponse, ResourceReference, RouteSection
from app.models.learning import (
    GeneratePlanRequest,
    GenerateRouteRequest,
    StudyPlanResponse,
    TeamCertificationAssignmentRequest,
    TeamCertificationAssignmentResponse,
    WeeklyMilestone,
)
from app.services._shared import response_data
from app.services.onboarding_catalog import CERTIFICATION_TRACK_HINTS
from app.services.profile_service import ensure_profile_for_user
from app.core.config import get_settings
from app.services.team_service import _ensure_manager_access

logger = logging.getLogger(__name__)


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


def _build_route_sections(track: str) -> list[RouteSection]:
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


def _create_route_for_user(user_id: str, target_certification: str, detected_level: str) -> CertificationRouteResponse:
    settings = get_settings()
    track = _resolve_track(target_certification)
    source_mode = "foundry" if foundry_enabled() else "mock"
    sections = _build_route_sections(track)
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
    )


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
    total_hours = sum(section.estimated_hours for section in sections)
    capacity = max(1, int(weekly_hours * 0.8))
    weeks_needed = max(1, (total_hours + capacity - 1) // capacity)
    deadline = (
        datetime.fromisoformat(requested_deadline.replace("Z", "+00:00"))
        if requested_deadline
        else datetime.now(timezone.utc) + timedelta(weeks=weeks_needed)
    )

    milestones: list[WeeklyMilestone] = []
    current_bucket: list[str] = []
    current_hours = 0
    week = 1
    for section in sections:
        if current_hours + section.estimated_hours > capacity and current_bucket:
            milestones.append(
                WeeklyMilestone(
                    week=week,
                    title=f"Semana {week}",
                    section_ids=current_bucket,
                    estimated_hours=current_hours,
                )
            )
            week += 1
            current_bucket = []
            current_hours = 0
        current_bucket.append(section.section_id)
        current_hours += section.estimated_hours
    if current_bucket:
        milestones.append(
            WeeklyMilestone(
                week=week,
                title=f"Semana {week}",
                section_ids=current_bucket,
                estimated_hours=current_hours,
            )
        )

    workiq_context = get_mock_calendar_context(preferred_time, weekly_hours)
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
    return CertificationRouteResponse(
        id=route["id"],
        target_certification=route["target_certification"],
        detected_level=route["detected_level"],
        source_mode=route["source_mode"],
        sections=[RouteSection.model_validate(item) for item in route["sections"]],
    )


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
    return StudyPlanResponse(
        id=plan["id"],
        route_id=plan["route_id"],
        target_certification=plan["target_certification"],
        deadline_at=plan["deadline_at"],
        weekly_hours=plan["weekly_hours"],
        weekly_milestones=[WeeklyMilestone.model_validate(item) for item in plan["weekly_milestones"]],
        workiq_context=plan["workiq_context"],
        status=plan["status"],
    )


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
