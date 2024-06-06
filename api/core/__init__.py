import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, env_ignore_empty=True):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "user"
    DB_PASS: str = "password"
    DB_NAME: str = "budget_bot"

    DB_ECHO: bool = False
    DB_TEST: bool = False

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = (
        "88dad50186c7acc55fbf555e8cbcf5ee" "a5c4afeed448b519f3672894c3c74938"
    )

    @property
    def db_url(self) -> str:
        if self.DB_TEST:
            return 'sqlite+aiosqlite:///testdb.db'

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
