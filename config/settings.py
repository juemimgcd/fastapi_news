# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fastapi_news"
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api"

    cors_origins: str = ""

    async_database_url: str
    redis_url: str

    model_config = SettingsConfigDict(
        env_file=".venv/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
