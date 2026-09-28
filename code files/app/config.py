from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FitBuddy"
    debug: bool = True
    database_url: str = "sqlite:///./fitbuddy.db"

    gemini_api_key: str = ""
    workout_model: str = "gemini-3.1-pro"
    fast_model: str = "gemini-3.8-flash"

    admin_token: str = "change-me"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
TEMPLATE_DIR = PROJECT_DIR / "templates"
STATIC_DIR = PROJECT_DIR / "static"
