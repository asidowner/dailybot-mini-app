from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardRemove, Update, User
from telegram.ext import ContextTypes

from bot.constants import (
    ALLOW_ID_ADDED_SUCCESSFUL,
    DAILY_COMMAND_TEXT,
    DAILY_DATA_TEXT,
    HELP_TEXT,
    ID_TEXT,
    START_TEXT,
    UNHANDLED_ERROR,
)
from bot.handlers import (
    END_KEYBOARD,
    START_KEYBOARD,
    add_user_to_allow_list,
    daily_command,
    error_handler,
    get_daily_result,
    help_command,
    id_command,
    start,
    start_over,
)


# Пример теста для команды /start
@pytest.mark.asyncio()
async def test_start() -> None:
    update = MagicMock(Update)
    context = MagicMock(ContextTypes.DEFAULT_TYPE)

    mock_user = MagicMock(User)
    mock_user.id = 12345
    update.message.from_user = mock_user
    update.message.reply_text = AsyncMock()

    with patch("bot.handlers.get_user_if_can_access", return_value=True):
        await start(update, context)

    update.message.reply_text.assert_called_once_with(
        text=START_TEXT, reply_markup=InlineKeyboardMarkup(START_KEYBOARD)
    )


# Пример теста для команды start_over
@pytest.mark.asyncio()
async def test_start_over() -> None:
    query = MagicMock(CallbackQuery)
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    query.from_user.id = 12345
    update = MagicMock(Update)
    update.callback_query = query
    context = MagicMock(ContextTypes.DEFAULT_TYPE)

    with patch("bot.handlers.get_user_if_can_access", return_value=True):
        await start_over(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once_with(text=START_TEXT, reply_markup=InlineKeyboardMarkup(START_KEYBOARD))


# Пример теста для команды help_command
@pytest.mark.asyncio()
async def test_help_command() -> None:
    query = MagicMock(CallbackQuery)
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock(Update)
    update.callback_query = query
    context = MagicMock(ContextTypes.DEFAULT_TYPE)

    await help_command(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once_with(text=HELP_TEXT, reply_markup=InlineKeyboardMarkup(END_KEYBOARD))


# Пример теста для команды id_command
@pytest.mark.asyncio()
async def test_id_command() -> None:
    query = MagicMock(CallbackQuery)
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    query.from_user.id = 12345
    update = MagicMock(Update)
    update.callback_query = query
    context = MagicMock(ContextTypes.DEFAULT_TYPE)

    await id_command(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once_with(
        text=ID_TEXT % 12345, reply_markup=InlineKeyboardMarkup(END_KEYBOARD)
    )


# Пример теста для команды daily_command
@pytest.mark.asyncio()
async def test_daily_command() -> None:
    query = MagicMock(CallbackQuery)
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock(Update)
    update.callback_query = query
    context = MagicMock(ContextTypes.DEFAULT_TYPE)

    await daily_command(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once_with(
        text=DAILY_COMMAND_TEXT, reply_markup=InlineKeyboardMarkup(END_KEYBOARD)
    )


# Пример теста для команды get_daily_result
@pytest.mark.asyncio()
async def test_get_daily_result() -> None:
    mock_user = MagicMock()
    mock_user.is_admin = True
    update = MagicMock(Update)
    update.message.reply_text = AsyncMock()
    update.message.reply_document = AsyncMock()
    context = MagicMock(ContextTypes.DEFAULT_TYPE)
    update.message.from_user.id = 12345

    with patch("bot.handlers.get_user_if_can_access", return_value=mock_user):
        with patch("bot.handlers.get_daily_data", return_value=[{"data": "some data"}]) as mock_get_daily_data:
            with patch("bot.handlers.build_daily_result", return_value="<html>Some result</html>"):
                await get_daily_result(update, context)
                update.message.reply_text.assert_called_once_with(text=DAILY_DATA_TEXT)
                update.message.reply_document.assert_called_once()
                mock_get_daily_data.assert_called_once()  # Убедитесь, что get_daily_data был вызван


# Пример теста для добавления пользователя в allow list
@pytest.mark.asyncio()
async def test_add_user_to_allow_list() -> None:
    mock_user = MagicMock()
    mock_user.is_admin = True
    update = MagicMock(Update)
    update.effective_message.reply_text = AsyncMock()
    context = MagicMock(ContextTypes.DEFAULT_TYPE)
    context.args = [67890]
    update.message.from_user.id = 12345

    with patch("bot.handlers.get_user_if_can_access", return_value=mock_user):
        with patch("bot.handlers.add_user_id_to_allow_access") as mock_add_user:
            await add_user_to_allow_list(update, context)
            mock_add_user.assert_called_once_with(67890)
            update.effective_message.reply_text.assert_called_once_with(text=ALLOW_ID_ADDED_SUCCESSFUL % 67890)


# Пример теста для обработки ошибок
@pytest.mark.asyncio()
async def test_error_handler() -> None:
    update = MagicMock(Update)
    update.effective_message.reply_text = AsyncMock()
    context = MagicMock(ContextTypes.DEFAULT_TYPE)
    context.error = Exception("Test error")

    await error_handler(update, context)

    update.effective_message.reply_text.assert_called_once_with(
        text=UNHANDLED_ERROR, reply_markup=ReplyKeyboardRemove()
    )
