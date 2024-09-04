from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from bot.database.database import session_maker
from bot.database.models import DailyModel, UserModel

if TYPE_CHECKING:
    from datetime import date


def get_daily_data(date_from: date) -> list[DailyModel]:
    session = session_maker()

    query = select(DailyModel).options(joinedload(DailyModel.user)).where(DailyModel.created_at >= date_from)
    return session.execute(query).scalars().fetchall()


def save_daily_data(user: UserModel, yesterday_tasks: str, today_plan: str, issues: str | None = None) -> None:
    session = session_maker()

    query = insert(DailyModel).values(
        user_id=user.id, yesterday_tasks=yesterday_tasks, today_plan=today_plan, issues=issues
    )
    session.execute(query)
    session.commit()
    session.close()
