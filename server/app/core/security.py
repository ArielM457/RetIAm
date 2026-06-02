from collections.abc import Mapping

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db.supabase import get_supabase_anon_client

security_scheme = HTTPBearer(auto_error=False)


def _get_user_property(user: object, field: str):
    if isinstance(user, Mapping):
        return user.get(field)
    return getattr(user, field, None)


def get_current_supabase_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )

    token = credentials.credentials
    try:
        result = get_supabase_anon_client().auth.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase session.",
        ) from exc

    user = _get_user_property(result, "user")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase session.",
        )

    return user
