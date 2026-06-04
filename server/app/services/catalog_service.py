from app.models.certification import CertificationSummary


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
    return CERTIFICATIONS
