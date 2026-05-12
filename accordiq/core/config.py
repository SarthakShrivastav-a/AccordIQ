from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    name: str
    slug: str
    version: str
    environment: str
    api_prefix: str
    config_version: int


class DatabaseSettings(BaseModel):
    url_env: str
    default_url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    vector_dimensions: int = 1024
    auto_create_tables: bool = False

    @property
    def url(self) -> str:
        return os.getenv(self.url_env, self.default_url)


class RedisSettings(BaseModel):
    url_env: str
    default_url: str
    dedupe_ttl_seconds: int
    queue_name: str

    @property
    def url(self) -> str:
        return os.getenv(self.url_env, self.default_url)


class SlackSettings(BaseModel):
    signing_secret_env: str
    client_id_env: str
    client_secret_env: str
    bot_token_env: str
    ack_timeout_seconds: int
    app_name: str
    command_name: str
    scopes: list[str]
    events: list[str]


class NotionSettings(BaseModel):
    api_version: str
    client_id_env: str
    client_secret_env: str
    database_name: str
    id_property: str
    requests_per_second: int


class ModelSettings(BaseModel):
    provider: str
    model: str
    temperature: float = 0
    api_key_env: str
    dimensions: int | None = None


class AISettings(BaseModel):
    extraction: ModelSettings
    judge: ModelSettings
    responder: ModelSettings
    embeddings: ModelSettings


class WorkflowSettings(BaseModel):
    confidence_threshold: float
    rewrite_limit: int
    top_k: int
    chunk_tokens: int
    chunk_overlap_tokens: int
    default_retention_days: int
    allowed_retention_days: list[int]
    query_intents: list[str]
    entity_types: list[str]


class CaptureSettings(BaseModel):
    default_mode: str
    ignore_bot_messages: bool
    include_private_channels_when_invited: bool
    pause_hours: int
    emojis: dict[str, str]


class SecuritySettings(BaseModel):
    encryption_key_env: str
    signature_tolerance_seconds: int
    redact_before_persistence: bool
    redaction_patterns: list[str]


class GoogleAuthSettings(BaseModel):
    client_id_env: str
    client_secret_env: str
    redirect_uri: str
    scopes: list[str]

    @property
    def client_id(self) -> str:
        return os.getenv(self.client_id_env, "")

    @property
    def client_secret(self) -> str:
        return os.getenv(self.client_secret_env, "")


class JwtSettings(BaseModel):
    secret_env: str
    algorithm: str
    issuer: str
    audience: str
    access_token_ttl_minutes: int

    @property
    def secret(self) -> str:
        return os.getenv(self.secret_env, "")


class InviteSettings(BaseModel):
    allowed_emails: list[str] = Field(default_factory=list)


class AuthSettings(BaseModel):
    google: GoogleAuthSettings
    jwt: JwtSettings
    invites: InviteSettings
    workspace_domain_map: dict[str, str] = Field(default_factory=dict)
    frontend_success_url: str
    frontend_error_url: str
    cors_origins: list[str] = Field(default_factory=list)


class SaasOnboardingSettings(BaseModel):
    required_steps: list[str]


class SaasUsageSettings(BaseModel):
    event_types: list[str]


class SaasIntegrationProviderSettings(BaseModel):
    provider: str
    status_values: list[str]


class SaasIntegrationSettings(BaseModel):
    slack: SaasIntegrationProviderSettings
    notion: SaasIntegrationProviderSettings


class SaasSettings(BaseModel):
    default_org_role: str
    default_member_role: str
    allowed_org_roles: list[str]
    onboarding: SaasOnboardingSettings
    usage: SaasUsageSettings
    integrations: SaasIntegrationSettings


class DockerSettings(BaseModel):
    image_repository: str
    dev_tag: str
    main_tag: str


class Settings(BaseModel):
    app: AppSettings
    database: DatabaseSettings
    redis: RedisSettings
    slack: SlackSettings
    notion: NotionSettings
    ai: AISettings
    workflow: WorkflowSettings
    capture: CaptureSettings
    security: SecuritySettings
    auth: AuthSettings
    saas: SaasSettings
    docker: DockerSettings
    raw: dict[str, Any] = Field(default_factory=dict)


def load_settings(path: str | Path | None = None) -> Settings:
    config_path = Path(path or os.getenv("ACCORDIQ_CONFIG_PATH", "config/app.yaml"))
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return Settings(**data, raw=data)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
