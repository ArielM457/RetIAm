from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "server"))

from app.core.config import get_settings  # noqa: E402


def main() -> None:
    settings = get_settings()
    checks = {
        "SUPABASE_URL": bool(settings.supabase_url),
        "SUPABASE_ANON_KEY": bool(settings.supabase_anon_key),
        "SUPABASE_SERVICE_ROLE_KEY": bool(settings.supabase_service_role_key),
        "AZURE_FOUNDRY_ENDPOINT": bool(settings.azure_foundry_endpoint),
        "AZURE_FOUNDRY_PROJECT": bool(settings.azure_foundry_project),
        "AZURE_FOUNDRY_API_KEY": bool(settings.azure_foundry_api_key),
        "AZURE_SEARCH_ENDPOINT": bool(settings.azure_search_endpoint),
        "AZURE_SEARCH_INDEX": bool(settings.azure_search_index),
        "WORKIQ_TENANT_ID": bool(settings.workiq_tenant_id),
        "WORKIQ_CLIENT_ID": bool(settings.workiq_client_id),
        "WORKIQ_CLIENT_SECRET": bool(settings.workiq_client_secret),
    }

    print("RetAIM external setup check")
    print()
    for key, ok in checks.items():
        print(f"{key}: {'OK' if ok else 'MISSING'}")


if __name__ == "__main__":
    main()
