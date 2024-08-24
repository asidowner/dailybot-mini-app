from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4

from psycopg import Connection
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__psycopg_{prefix}_{uuid4()}__"


def get_engine(url: URL | str = settings.database_url) -> Engine:
    return create_engine(
        url=url,
        echo=settings.DEBUG,
        pool_size=0,
        connect_args={
            "connection_class": CConnection,
        },
    )


def get_session_maker(engine_: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine_, autoflush=False, expire_on_commit=False)


db_url = settings.database_url
engine = get_engine(url=db_url)
session_maker = get_session_maker(engine)
