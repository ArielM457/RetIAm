from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RetAIM Server"
    app_env: str = "development"
    api_prefix: str = "/api"
    client_url: str = "http://localhost:4200"

    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_profiles_table: str = "profiles"

    blocked_email_domains: str = (
        "gmail.com,hotmail.com,outlook.com,yahoo.com,icloud.com,live.com"
    )

    model_config = SettingsConfigDict(
        env_file=(".env", "server/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def blocked_domains(self) -> set[str]:
        return {
            domain.strip().lower()
            for domain in self.blocked_email_domains.split(",")
            if domain.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
