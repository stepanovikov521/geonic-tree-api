import logging

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Основные настройки приложения."""

    app_name: str = "Geonic Tree"
    debug: bool = False
    database_url: str = Field(default="")
    secret_key: SecretStr = Field(default=SecretStr(""))
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    log_level: str = "INFO"


model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding="utf-8", extra="ignore"
)


@model_validator(mode="after")
def validate_settings(self) -> "Settings":
    """Проверка, что критически важные настройки были загружены из окружения."""
    if not self.database_url:
        raise ValueError(
            "DATABASE_URL must be set in the environment (e.g., in .env file)"
        )
    if not self.secret_key.get_secret_value():
        raise ValueError(
            "SECRET_KEY must be set in the environment (e.g., in .env file)"
        )
    return self


settings = Settings()

# Настройка единого логгера для всего проекта
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("geonic_tree")
