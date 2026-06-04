from app.core.config import get_settings


def foundry_enabled() -> bool:
    settings = get_settings()
    return bool(
        settings.enable_external_ai
        and settings.azure_foundry_endpoint
        and settings.azure_foundry_project
        and settings.azure_foundry_api_key
    )
