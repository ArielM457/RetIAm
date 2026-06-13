from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_supabase_user
from app.models.course import CourseCatalogSummary, CourseDetail
from app.services.course_service import get_course_detail, list_courses
from app.services.profile_service import ensure_profile_for_user
from app.services.team_service import get_user_team_ids

router = APIRouter()


@router.get("", response_model=list[CourseCatalogSummary])
def get_courses(current_user=Depends(get_current_supabase_user)) -> list[CourseCatalogSummary]:
    # Scoping: los cursos personalizados solo se ven si perteneces a ese equipo.
    profile = ensure_profile_for_user(current_user)
    return list_courses(get_user_team_ids(profile.id))


@router.get("/{certification_code}", response_model=CourseDetail)
def get_course(
    certification_code: str,
    current_user=Depends(get_current_supabase_user),
) -> CourseDetail:
    course = get_course_detail(certification_code)
    if not course:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No hay curso cargado para {certification_code}. "
                "Corre la ingesta de contenido (infra/ingest_content.py)."
            ),
        )
    return course
