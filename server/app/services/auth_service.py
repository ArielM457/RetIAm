from email.utils import parseaddr

from app.core.config import get_settings


def validate_corporate_email(email: str) -> bool:
    _, normalized = parseaddr(email)
    if "@" not in normalized:
        return False

    domain = normalized.rsplit("@", 1)[-1].lower()
    return domain not in get_settings().blocked_domains
