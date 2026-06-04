from pydantic import BaseModel


class IntegrationStatusResponse(BaseModel):
    foundry_enabled: bool
    workiq_enabled: bool
    foundry_endpoint_configured: bool
    search_index_configured: bool
    supabase_configured: bool
    notes: list[str]
