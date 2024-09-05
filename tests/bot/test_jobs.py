from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from core.config import settings

from bot.constants import (
    DAILY_JOBS_COMMAND_TEXT,
    DAILY_UPDATE_KEYBOARD_TEXT,
    DAILY_UPDATE_TEXT,
)
from bot.jobs import (
    daily_reminder_handler,
    daily_update_reminder_handler,
)


# Тест для daily_update_reminder_handler с мокированием get_users
@pytest.mark.asyncio()
async def test_daily_update_reminder_handler() -> None:
    context = MagicMock()
    context.bot.send_message = AsyncMock()

    mock_users = [MagicMock(id=1), MagicMock(id=2)]

    # Мокируем get_users, чтобы он возвращал заранее определенных пользователей
    with patch("bot.jobs.get_users", return_value=mock_users):
        await daily_update_reminder_handler(context)

    expected_markup = ReplyKeyboardMarkup.from_button(
        KeyboardButton(
            text=DAILY_UPDATE_KEYBOARD_TEXT,
            web_app=WebAppInfo(url=settings.daily_mini_app_url),
        )
    )

    context.bot.send_message.assert_any_call(1, DAILY_UPDATE_TEXT, reply_markup=expected_markup)
    context.bot.send_message.assert_any_call(2, DAILY_UPDATE_TEXT, reply_markup=expected_markup)
    assert context.bot.send_message.call_count == 2


# Тест для daily_reminder_handler с мокированием get_users
@pytest.mark.asyncio()
async def test_daily_reminder_handler() -> None:
    context = MagicMock()
    context.bot.send_message = AsyncMock()

    mock_users = [MagicMock(id=1), MagicMock(id=2)]

    # Мокируем get_users, чтобы он возвращал заранее определенных пользователей
    with patch("bot.jobs.get_users", return_value=mock_users):
        await daily_reminder_handler(context)

    context.bot.send_message.assert_any_call(1, DAILY_JOBS_COMMAND_TEXT)
    context.bot.send_message.assert_any_call(2, DAILY_JOBS_COMMAND_TEXT)
    assert context.bot.send_message.call_count == 2
