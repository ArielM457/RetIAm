from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_supabase_user
from app.models.course import CourseCatalogSummary, CourseDetail
from app.services.course_service import get_course_detail, list_courses

router = APIRouter()


@router.get("", response_model=list[CourseCatalogSummary])
def get_courses(current_user=Depends(get_current_supabase_user)) -> list[CourseCatalogSummary]:
    return list_courses()


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
