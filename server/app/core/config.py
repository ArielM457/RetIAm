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
    supabase_organizations_table: str = "organizations"
    supabase_teams_table: str = "teams"
    supabase_team_members_table: str = "team_members"
    supabase_team_invitations_table: str = "team_invitations"
    supabase_team_access_codes_table: str = "team_access_codes"
    supabase_profile_assessments_table: str = "profile_assessments"
    supabase_learning_routes_table: str = "learning_routes"
    supabase_study_plans_table: str = "study_plans"
    supabase_team_cert_assignments_table: str = "team_certification_assignments"
    supabase_learning_sessions_table: str = "learning_sessions"
    supabase_coach_reminders_table: str = "coach_reminders"
    supabase_suggestions_table: str = "suggestions"
    supabase_exam_attempts_table: str = "exam_attempts"
    supabase_certificates_table: str = "certificates"
    supabase_integrity_events_table: str = "integrity_events"
    supabase_courses_table: str = "courses"
    supabase_course_sections_table: str = "course_sections"
    supabase_course_lessons_table: str = "course_lessons"
    supabase_course_labs_table: str = "course_labs"
    supabase_lesson_completions_table: str = "lesson_completions"
    supabase_lesson_chat_messages_table: str = "lesson_chat_messages"
    supabase_course_enrollments_table: str = "course_enrollments"
    supabase_learning_agenda_items_table: str = "learning_agenda_items"
    supabase_lesson_chunks_table: str = "lesson_chunks"
    # Embeddings para el RAG (Supabase pgvector). multilingual-e5-large = 1024 dim,
    # multilingue, gratis y soportado por fastembed (usa prefijos query:/passage:).
    # Si cambias a un modelo de otra dimension, ajusta vector(1024) en supabase/schema.sql.
    embedding_model: str = "intfloat/multilingual-e5-large"
    embedding_dim: int = 1024

    public_email_domains: str = (
        "gmail.com,hotmail.com,outlook.com,yahoo.com,icloud.com,live.com"
    )
    azure_foundry_endpoint: str | None = None
    azure_foundry_project: str | None = None
    azure_foundry_deployment: str | None = None
    azure_foundry_api_key: str | None = None
    azure_foundry_api_version: str = "2024-10-21"
    azure_search_endpoint: str | None = None
    azure_search_key: str | None = None
    azure_search_index: str | None = None
    azure_blob_connection_string: str | None = None
    workiq_tenant_id: str | None = None
    workiq_client_id: str | None = None
    workiq_client_secret: str | None = None
    enable_external_ai: bool = False

    model_config = SettingsConfigDict(
        env_file=(".env", "server/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def public_domains(self) -> set[str]:
        return {
            domain.strip().lower()
            for domain in self.public_email_domains.split(",")
            if domain.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
