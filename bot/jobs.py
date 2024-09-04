from __future__ import annotations
from typing import TYPE_CHECKING

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from core.config import settings

from bot.services.user import get_users

if TYPE_CHECKING:
    from telegram.ext import Application, ContextTypes

DAILY_UPDATE_TEXT = "Жмакай на кнопку и заполни дейли апдейт."
DAILY_UPDATE_KEYBOARD_TEXT = "Жмак, жмак."
DAILY_COMMAND_TEXT = f"Ну и почему ты еще не на дейли? М?" f"Заходи сюда если, что:\n\n{settings.daily_place}"


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
            DAILY_COMMAND_TEXT,
        )


def add_jobs(application: Application) -> None:
    application.job_queue.run_daily(daily_update_reminder_handler, time=settings.daily_message_time)
    application.job_queue.run_daily(daily_reminder_handler, time=settings.daily_time)
