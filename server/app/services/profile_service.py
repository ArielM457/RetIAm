from collections.abc import Mapping

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.profile import UserProfileResponse


def _read_field(source: object, key: str, default=None):
    if isinstance(source, Mapping):
        return source.get(key, default)
    return getattr(source, key, default)


def ensure_profile_for_user(auth_user: object) -> UserProfileResponse:
    settings = get_settings()
    supabase = get_supabase_service_client()
    metadata = _read_field(auth_user, "user_metadata", {}) or {}
    email = _read_field(auth_user, "email")
    user_id = _read_field(auth_user, "id")

    payload = {
        "id": user_id,
        "email": email,
        "full_name": metadata.get("full_name"),
        "role": metadata.get("role", "employee"),
        "learning_style": metadata.get("learning_style", []),
    }

    try:
        response = (
            supabase.table(settings.supabase_profiles_table)
            .upsert(payload, on_conflict="id")
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "No se pudo sincronizar el perfil en Supabase. "
                "Revisa server/.env y supabase/schema.sql."
            ),
        ) from exc

    if isinstance(response.data, list):
        data = response.data[0] if response.data else payload
    else:
        data = response.data or payload

    return UserProfileResponse.model_validate(data)
