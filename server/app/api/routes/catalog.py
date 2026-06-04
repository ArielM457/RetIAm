from fastapi import APIRouter

from app.models.certification import CertificationSummary
from app.services.catalog_service import list_certifications

router = APIRouter()


@router.get("/certifications", response_model=list[CertificationSummary])
def get_certifications() -> list[CertificationSummary]:
    return list_certifications()
