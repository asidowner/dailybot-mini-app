from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


def get_engine(url: URL | str = settings.database_url) -> Engine:
    return create_engine(
        url=url,
        echo=settings.debug,
        pool_size=0,
    )


def get_session_maker(engine_: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine_, autoflush=True, expire_on_commit=False)


db_url = settings.database_url
engine = get_engine(url=db_url)
session_maker = get_session_maker(engine)
