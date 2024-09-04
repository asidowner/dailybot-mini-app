from __future__ import annotations
import datetime
from typing import Annotated

from sqlalchemy import BigInteger, ForeignKey, Sequence, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TABLE_ID = Sequence("table_id_seq", start=1)

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False)]
auto_big_int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True, type_=BigInteger)]
big_int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False, type_=BigInteger)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    repr_cols_num: int = 3  # print first columns
    repr_cols: tuple = ()  # extra printed columns

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


daily_id_seq = Sequence("daily_id_seq", start=1, increment=1)


class DailyModel(Base):
    __tablename__ = "daily"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, server_default=daily_id_seq.next_value())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship(back_populates="dailies")

    created_at: Mapped[created_at]

    yesterday_tasks: Mapped[str]
    today_plan: Mapped[str]
    issues: Mapped[str] = mapped_column(default=None, nullable=True)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[big_int_pk]
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    created_at: Mapped[created_at]

    dailies: Mapped[list[DailyModel]] = relationship(back_populates="user")

    is_admin: Mapped[bool] = mapped_column(default=False)
    is_block: Mapped[bool] = mapped_column(default=False)


class AllowedIdModel(Base):
    __tablename__ = "allowed_ids"

    id: Mapped[big_int_pk]
