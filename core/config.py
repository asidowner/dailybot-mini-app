from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    bot_token: str


class DBSettings(EnvBaseSettings):
    db_host: str = "postgres"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str | None = None
    db_name: str = "postgres"

    @property
    def database_url_psycopg(self) -> str:
        if self.DB_PASS:
            return f"postgresql+psycopg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        return f"postgresql+psycopg://{self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}"


class Settings(BotSettings, DBSettings):
    sentry_dsn: str | None = None


settings = Settings()
