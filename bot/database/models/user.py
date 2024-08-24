from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base import Base, big_int_pk, created_at


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[big_int_pk]
    username: Mapped[str | None]
    created_at: Mapped[created_at]

    is_admin: Mapped[bool] = mapped_column(default=False)
    is_block: Mapped[bool] = mapped_column(default=False)
