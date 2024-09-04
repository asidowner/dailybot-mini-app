from __future__ import annotations
from typing import TYPE_CHECKING

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from core.config import settings

from bot.constants import (
    DAILY_JOBS_COMMAND_TEXT,
    DAILY_UPDATE_KEYBOARD_TEXT,
    DAILY_UPDATE_TEXT,
)
from bot.services.user import get_users

if TYPE_CHECKING:
    from telegram.ext import Application, ContextTypes


async def daily_update_reminder_handler(context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_users()

    for user in users:
        await context.bot.send_message(
            user.id,
            DAILY_UPDATE_TEXT,
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text=DAILY_UPDATE_KEYBOARD_TEXT,
                    web_app=WebAppInfo(url=settings.daily_mini_app_url),
                )
            ),
        )


async def daily_reminder_handler(context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_users()

    for user in users:
        await context.bot.send_message(
            user.id,
            DAILY_JOBS_COMMAND_TEXT,
        )


def add_jobs(application: Application) -> Application:
    application.job_queue.run_daily(daily_update_reminder_handler, time=settings.daily_message_time)
    application.job_queue.run_daily(daily_reminder_handler, time=settings.daily_time)

    return application
