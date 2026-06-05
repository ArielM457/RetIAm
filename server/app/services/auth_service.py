from email.utils import parseaddr
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.db.supabase import get_supabase_anon_client, get_supabase_service_client
from app.models.auth import (
    AuthSessionResponse,
    AuthenticatedUserSummary,
    EmailValidationResponse,
    LoginRequest,
    RegisterRequest,
)
from app.services._shared import read_field
from app.services.profile_service import ensure_profile_for_user


def normalize_email(email: str) -> str:
    _, normalized = parseaddr(email)
    return normalized.strip().lower()


def analyze_email_address(email: str) -> EmailValidationResponse:
    normalized = normalize_email(email)
    if "@" not in normalized:
        return EmailValidationResponse(
            email=email,
            is_valid=False,
            is_corporate_domain=False,
            should_recommend_custom_domain=False,
            message="Ingresa un correo valido para continuar.",
        )

    domain = normalized.rsplit("@", 1)[-1]
    is_public_domain = domain in get_settings().public_domains
    recommendation = (
        "Recomendamos usar un dominio institucional o del equipo para la demo."
        if is_public_domain
        else "Excelente. Ese dominio ya luce alineado a una institucion o equipo."
    )
    message = (
        "Correo valido. Puedes seguir con este correo."
        if not is_public_domain
        else "Correo valido. Puedes seguir, aunque recomendamos usar un dominio propio del equipo."
    )

    return EmailValidationResponse(
        email=normalized,
        is_valid=True,
        is_corporate_domain=not is_public_domain,
        should_recommend_custom_domain=is_public_domain,
        recommendation=recommendation,
        message=message,
    )


def _get_active_team_access_code_or_raise(code: str) -> dict:
    normalized_code = code.strip().upper()
    if not normalized_code:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ingresa un codigo de equipo valido.",
        )

    settings = get_settings()
    response = (
        get_supabase_service_client()
        .table(settings.supabase_team_access_codes_table)
        .select("*")
        .eq("code", normalized_code)
        .eq("status", "active")
        .limit(1)
        .execute()
    )
    data = read_field(response, "data") or []
    code_data = data[0] if data else None
    if not code_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No encontramos un codigo activo con ese valor.",
        )

    if datetime.fromisoformat(code_data["expires_at"].replace("Z", "+00:00")) < datetime.now(timezone.utc):
        get_supabase_service_client().table(settings.supabase_team_access_codes_table).update(
            {"status": "expired"}
        ).eq("id", code_data["id"]).execute()
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ese codigo ya vencio. Pide uno nuevo al manager.",
        )

    return code_data


def _attach_employee_to_team(user_id: str, code_data: dict) -> None:
    settings = get_settings()
    get_supabase_service_client().table(settings.supabase_profiles_table).update(
        {
            "org_id": code_data["org_id"],
            "team_id": code_data["team_id"],
            "role": "employee",
        }
    ).eq("id", user_id).execute()

    get_supabase_service_client().table(settings.supabase_team_members_table).upsert(
        {
            "team_id": code_data["team_id"],
            "user_id": user_id,
        }
    ).execute()

    get_supabase_service_client().table(settings.supabase_team_access_codes_table).update(
        {
            "status": "used",
            "used_by": user_id,
            "used_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", code_data["id"]).execute()


def register_mock_user(payload: RegisterRequest) -> AuthSessionResponse:
    assessment = analyze_email_address(payload.email)
    if not assessment.is_valid:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=assessment.message)

    active_team_code: dict | None = None
    if payload.role == "employee" and payload.team_access_code:
        active_team_code = _get_active_team_access_code_or_raise(payload.team_access_code)

    try:
        created_user = get_supabase_service_client().auth.admin.create_user(
            {
                "email": assessment.email,
                "password": payload.password,
                "email_confirm": True,
                "user_metadata": {
                    "full_name": payload.full_name,
                    "role": payload.role,
                },
            }
        )
    except Exception as exc:
        detail = str(exc)
        if "already been registered" in detail.lower() or "user already registered" in detail.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ese correo ya existe. Inicia sesion o usa otro correo.",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo registrar el usuario en Supabase.",
        ) from exc

    auth_response = sign_in_mock_user(
        LoginRequest(email=assessment.email, password=payload.password),
        success_message="Cuenta creada correctamente para la demo.",
    )

    profile = ensure_profile_for_user(read_field(created_user, "user"))
    if active_team_code:
        _attach_employee_to_team(profile.id, active_team_code)
        auth_response = sign_in_mock_user(
            LoginRequest(email=assessment.email, password=payload.password),
            success_message="Cuenta creada y asociada al equipo correctamente.",
        )
    return auth_response


def sign_in_mock_user(
    payload: LoginRequest,
    *,
    success_message: str = "Sesion iniciada correctamente.",
) -> AuthSessionResponse:
    assessment = analyze_email_address(payload.email)
    if not assessment.is_valid:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=assessment.message)

    try:
        response = get_supabase_anon_client().auth.sign_in_with_password(
            {"email": assessment.email, "password": payload.password}
        )
    except Exception as exc:
        detail = str(exc).lower()
        if "invalid login credentials" in detail:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No encontramos una sesion valida con ese correo y contrasena. Si no tienes cuenta, registrate primero.",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo iniciar sesion contra Supabase.",
        ) from exc

    session = read_field(response, "session")
    user = read_field(response, "user")
    if not session or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Supabase no devolvio una sesion utilizable.",
        )

    profile = ensure_profile_for_user(user)
    return AuthSessionResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        token_type=session.token_type,
        expires_in=session.expires_in,
        expires_at=session.expires_at,
        user=AuthenticatedUserSummary(
            id=profile.id,
            email=profile.email,
            full_name=profile.full_name,
            role=profile.role,
            org_id=profile.org_id,
            team_id=profile.team_id,
        ),
        message=success_message,
    )
