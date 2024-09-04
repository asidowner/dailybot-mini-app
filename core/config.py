from __future__ import annotations
import datetime
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    bot_token: str
    admin_user_ids: list[int] = []


class DailySettings(EnvBaseSettings):
    daily_mini_app_url: str
    daily_place: str
    daily_time: datetime.time = datetime.time(
        hour=10,
        minute=15,
        second=0,
        tzinfo=datetime.timezone(datetime.timedelta(hours=3)),
    )
    daily_message_time: datetime.time = datetime.time(
        hour=10,
        minute=0,
        second=0,
        tzinfo=datetime.timezone(datetime.timedelta(hours=3)),
    )


class DBSettings(EnvBaseSettings):
    db_host: str = "postgres"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str | None = None
    db_name: str = "postgres"

    @property
    def database_url(self) -> str:
        if self.db_pass:
            return f"postgresql+psycopg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        return f"postgresql+psycopg://{self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}"


class Settings(BotSettings, DBSettings, DailySettings):
    debug: bool = False
    sentry_dsn: str | None = None
    base_path: str | None = os.path.realpath(__file__)
    timezone_offset: int = 3


settings = Settings()
