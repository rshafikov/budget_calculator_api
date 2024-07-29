import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PWD = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings, env_ignore_empty=True):
    model_config = SettingsConfigDict(
        env_file=PWD / '.env',
        env_file_encoding="utf-8"
    )

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "user"
    DB_PASS: str = "password"
    DB_NAME: str = "budget_bot"

    DB_ECHO: bool = False
    DB_TEST: bool | str = False

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = (
        "88dad50186c7acc55fbf555e8cbcf5ee" "a5c4afeed448b519f3672894c3c74938"
    )

    @property
    def db_url(self) -> str:
        if self.DB_TEST or os.environ.get('DB_TEST'):
            return 'sqlite+aiosqlite:///:memory:'

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def project_dir(self) -> Path:
        return PWD


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
