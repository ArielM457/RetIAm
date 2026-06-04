from app.core.config import get_settings
from app.integrations.foundry_adapter import foundry_enabled
from app.integrations.workiq_adapter import workiq_enabled
from app.models.integration import IntegrationStatusResponse


def get_integration_status() -> IntegrationStatusResponse:
    settings = get_settings()
    notes = [
        "Completa las variables de Azure AI Foundry para usar contenido fundamentado real.",
        "Completa las credenciales de Work IQ o Microsoft Graph para señales reales de calendario.",
        "Mientras esas variables no esten listas, el backend usa comportamiento mock seguro para la demo.",
    ]
    return IntegrationStatusResponse(
        foundry_enabled=foundry_enabled(),
        workiq_enabled=workiq_enabled(),
        foundry_endpoint_configured=bool(settings.azure_foundry_endpoint),
        search_index_configured=bool(settings.azure_search_index),
        supabase_configured=bool(
            settings.supabase_url and settings.supabase_anon_key and settings.supabase_service_role_key
        ),
        notes=notes,
    )
