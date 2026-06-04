from pydantic import BaseModel, Field


class CertificationSummary(BaseModel):
    code: str
    title: str
    provider: str
    level: str
    description: str
    recommended_for: list[str] = Field(default_factory=list)


class ResourceReference(BaseModel):
    title: str
    type: str
    source: str
    url: str


class RouteSection(BaseModel):
    section_id: str
    title: str
    order: int
    estimated_hours: int
    resources: list[ResourceReference] = Field(default_factory=list)
    prerequisite_sections: list[str] = Field(default_factory=list)


class CertificationRouteResponse(BaseModel):
    id: str | None = None
    target_certification: str
    detected_level: str
    source_mode: str
    sections: list[RouteSection] = Field(default_factory=list)
