"""Settings: secrets from env/.env, non-secret knobs from deskflow.config.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RelevanceRubric(BaseModel):
    High: str
    Medium: str
    Low: str


class ProjectConfig(BaseModel):
    """Non-secret, user-editable settings loaded from deskflow.config.yaml."""

    topics: list[str]
    research_interests: str
    relevance_rubric: RelevanceRubric
    lookback_days: int = Field(gt=0)
    schedule_cron: str

    @field_validator("topics")
    @classmethod
    def topics_non_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("deskflow.config.yaml: topics must not be empty")
        return v


class Settings(BaseSettings):
    """Secrets and provider selection, loaded from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    notion_token: str = ""
    notion_database_id: str = ""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    llm_provider: str = "ollama"
    ollama_model: str = "mistral"
    ollama_host: str = "http://localhost:11434"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    deskflow_config_path: str = "deskflow.config.yaml"

    @field_validator(
        "notion_token",
        "telegram_bot_token",
        "gemini_api_key",
        mode="before",
    )
    @classmethod
    def strip_secret(cls, v: str | None) -> str:
        return (v or "").strip()


def load_project_config(path: str | Path = "deskflow.config.yaml") -> ProjectConfig:
    raw = yaml.safe_load(Path(path).read_text())
    return ProjectConfig.model_validate(raw)


settings = Settings()
project_config = load_project_config(settings.deskflow_config_path)
