import logging

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.certification import CertificationSummary
from app.services._shared import response_data

logger = logging.getLogger(__name__)


# Catalogo curado de respaldo: se usa solo si la tabla `courses` esta vacia
# (p.ej. antes de correr la ingesta). Una vez ingeridos los cursos, el catalogo
# se sirve desde Supabase.
CERTIFICATIONS = [
    CertificationSummary(
        code="AZ-900",
        title="Microsoft Azure Fundamentals",
        provider="Microsoft",
        level="basic",
        description="Fundamentos de nube y servicios principales de Azure.",
        recommended_for=["backend", "frontend", "devops", "data"],
    ),
    CertificationSummary(
        code="AZ-204",
        title="Developing Solutions for Microsoft Azure",
        provider="Microsoft",
        level="intermediate",
        description="Desarrollo de aplicaciones cloud en Azure.",
        recommended_for=["backend", "fullstack", "cloud"],
    ),
    CertificationSummary(
        code="AWS Cloud Practitioner",
        title="AWS Certified Cloud Practitioner",
        provider="Amazon",
        level="basic",
        description="Fundamentos generales de servicios AWS.",
        recommended_for=["backend", "cloud", "devops"],
    ),
    CertificationSummary(
        code="GitHub Foundations",
        title="GitHub Foundations",
        provider="GitHub",
        level="basic",
        description="Colaboracion, automatizacion y seguridad en GitHub.",
        recommended_for=["backend", "frontend", "devops", "qa"],
    ),
]


def list_certifications() -> list[CertificationSummary]:
    """Lista el catalogo desde la tabla `courses` (una sola query). Cae al curado si esta vacia."""
    settings = get_settings()
    try:
        rows = response_data(
            get_supabase_service_client()
            .table(settings.supabase_courses_table)
            .select("certification_code,title,provider,level,summary,track")
            .order("track")
            .order("title")
            .execute(),
            [],
        ) or []
    except Exception as exc:
        logger.warning("No se pudo leer el catalogo de cursos; uso el curado: %s", exc)
        return CERTIFICATIONS

    if not rows:
        return CERTIFICATIONS

    return [
        CertificationSummary(
            code=row["certification_code"],
            title=row.get("title") or row["certification_code"],
            provider=row.get("provider") or (row.get("track") or "").title(),
            level=row.get("level") or "basic",
            description=row.get("summary") or "",
            recommended_for=[row["track"]] if row.get("track") else [],
        )
        for row in rows
    ]
