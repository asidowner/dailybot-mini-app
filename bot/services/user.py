from __future__ import annotations

from sqlalchemy import exists, select
from sqlalchemy.dialects.postgresql import insert

from core.config import settings

from bot.database.database import session_maker
from bot.database.models import AllowedIdModel, UserModel


def get_user(user_id: int) -> UserModel | None:
    session = session_maker()

    query = select(UserModel).where(UserModel.id == user_id).where(UserModel.is_block.is_(False))

    return session.execute(query).scalars().one_or_none()


def get_users() -> list[UserModel]:
    session = session_maker()

    query = select(UserModel).where(UserModel.is_block is False)

    with session.begin():
        return session.execute(query).scalars().all()


def is_allow_access(user_id: int) -> bool:
    session = session_maker()

    query = exists().where(AllowedIdModel.id == user_id).select()

    return session.execute(query).fetchone()[0]


def add_user_id_to_allow_access(user_id: int) -> None:
    session = session_maker()
    query = insert(AllowedIdModel).values(id=user_id).on_conflict_do_nothing()

    with session.begin():
        session.execute(query)
        session.commit()


def add_user(user_id: int, username: str, first_name: str | None = None, last_name: str | None = None) -> UserModel:
    session = session_maker()

    is_admin = user_id in settings.admin_user_ids

    query = (
        insert(UserModel)
        .values(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            is_block=False,
        )
        .on_conflict_do_update(
            constraint="users_pkey",
            set_={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "is_admin": is_admin,
            },
        )
        .returning(UserModel)
    )

    with session.begin():
        result = session.execute(query).scalars().one()
        session.commit()
    return result
