from pydantic import BaseModel, Field


class SuggestionRequest(BaseModel):
    category: str
    message: str


class SuggestionResponse(BaseModel):
    id: str | None = None
    category: str
    message: str
    status: str
    agent_response: str
    created_at: str | None = None


class TeamSuggestionSummary(BaseModel):
    team_id: str
    totals_by_category: dict = Field(default_factory=dict)
    totals_by_status: dict = Field(default_factory=dict)
