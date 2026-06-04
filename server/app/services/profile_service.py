from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_service_client
from app.models.profile import UpdateMyProfileRequest, UserProfileResponse
from app.services._shared import read_field, response_data


def ensure_profile_for_user(auth_user: object) -> UserProfileResponse:
    settings = get_settings()
    supabase = get_supabase_service_client()
    metadata = read_field(auth_user, "user_metadata", {}) or {}
    email = read_field(auth_user, "email")
    user_id = read_field(auth_user, "id")

    payload = {
        "id": user_id,
        "email": email,
        "full_name": metadata.get("full_name"),
        "role": metadata.get("role", "employee"),
        "professional_role": metadata.get("professional_role"),
        "learning_style": metadata.get("learning_style", []),
        "profile_version": 1,
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

    raw_data = response_data(response, payload)
    if isinstance(raw_data, list):
        data = raw_data[0] if raw_data else payload
    else:
        data = raw_data or payload

    return UserProfileResponse.model_validate(data)


def update_my_profile(user_id: str, payload: UpdateMyProfileRequest) -> UserProfileResponse:
    settings = get_settings()
    update_payload = payload.model_dump(exclude_none=True)
    if not update_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No recibimos campos para actualizar.",
        )

    response = (
        get_supabase_service_client()
        .table(settings.supabase_profiles_table)
        .update(update_payload)
        .eq("id", user_id)
        .execute()
    )
    raw_data = response_data(response, [])
    data = raw_data[0] if isinstance(raw_data, list) and raw_data else None
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado.")
    return UserProfileResponse.model_validate(data)
