from __future__ import annotations
from typing import TYPE_CHECKING

from jinja2 import Environment, PackageLoader, select_autoescape

if TYPE_CHECKING:
    from datetime import date

    from bot.database.models import DailyModel

env = Environment(loader=PackageLoader("bot", "templates"), autoescape=select_autoescape())


def build_daily_result(date_from: date, daily_data: list[DailyModel]) -> str:
    template = env.get_template("daily_report.html")

    return template.render(
        data=[
            {
                "name": f"{data.user.last_name} {data.user.first_name}",
                "yesterday_tasks": data.yesterday_tasks,
                "today_plan": data.today_plan,
                "issues": data.issues,
            }
            for data in daily_data
        ],
        date=date_from,
    )
