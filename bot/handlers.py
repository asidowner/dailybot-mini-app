from __future__ import annotations
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update, User
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from core.config import settings

from bot.constants import (
    ALLOW_ID_ADDED_SUCCESSFUL,
    DAILY_COMMAND_TEXT,
    DAILY_DATA_IS_EMPTY_TEXT,
    DAILY_DATA_SAVE_MESSAGE,
    DAILY_DATA_TEXT,
    HELP_TEXT,
    ID_TEXT,
    NOT_ALLOWED_MESSAGE,
    START_TEXT,
    UNHANDLED_ERROR,
)
from bot.misc import build_daily_result
from bot.services.daily import get_daily_data, save_daily_data
from bot.services.user import add_user, add_user_id_to_allow_access, get_user, is_allow_access

if TYPE_CHECKING:
    from bot.database.models import UserModel

START_ROUTES, END_ROUTES = range(2)

HELP, ID, DAILY, END = range(4)

logger = logging.getLogger(__name__)

START_KEYBOARD = [
    [
        InlineKeyboardButton("Помощь", callback_data=HELP),
        InlineKeyboardButton("Мой ID", callback_data=ID),
        InlineKeyboardButton("Дейли", callback_data=DAILY),
    ]
]

NO_AUTH_START_KEYBOARD = [
    [
        InlineKeyboardButton("Мой ID", callback_data=ID),
    ]
]

END_KEYBOARD = [
    [
        InlineKeyboardButton("Назад", callback_data=END),
    ]
]


def get_user_if_can_access(chat_user: User) -> UserModel | None:
    user = get_user(chat_user.id)
    if not user and is_allow_access(chat_user.id):
        return add_user(chat_user.id, chat_user.username, chat_user.first_name, chat_user.last_name)
    return user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # noqa: ARG001
    """Send message on `/start`."""
    chat_user = update.message.from_user

    user = get_user_if_can_access(chat_user)

    logger.info("User %s started the conversation with id %s.", chat_user.first_name, chat_user.id)

    keyboard = START_KEYBOARD if user else NO_AUTH_START_KEYBOARD

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text=START_TEXT, reply_markup=reply_markup)

    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # noqa: ARG001
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query

    await query.answer()

    user = get_user_if_can_access(query.from_user)

    keyboard = START_KEYBOARD if user else NO_AUTH_START_KEYBOARD
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=START_TEXT, reply_markup=reply_markup)
    return START_ROUTES


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # noqa: ARG001
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(END_KEYBOARD)

    await query.edit_message_text(
        text=HELP_TEXT,
        reply_markup=reply_markup,
    )

    return END_ROUTES


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # noqa: ARG001
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(END_KEYBOARD)

    await query.edit_message_text(
        text=ID_TEXT % query.from_user.id,
        reply_markup=reply_markup,
    )

    return END_ROUTES


async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # noqa: ARG001
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(END_KEYBOARD)

    await query.edit_message_text(
        text=DAILY_COMMAND_TEXT,
        reply_markup=reply_markup,
    )

    return END_ROUTES


async def get_daily_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001
    user = get_user_if_can_access(update.message.from_user)

    if not user or not user.is_admin:
        await update.message.reply_text(
            text=NOT_ALLOWED_MESSAGE,
        )
        return

    date_from = datetime.now(timezone(timedelta(hours=settings.timezone_offset))).date()
    daily_data = get_daily_data(date_from)

    if not daily_data:
        await update.message.reply_text(
            text=DAILY_DATA_IS_EMPTY_TEXT,
        )
    else:
        message = build_daily_result(date_from, daily_data)
        await update.message.reply_text(
            text=DAILY_DATA_TEXT,
        )
        await update.message.reply_document(
            document=bytes(message, "utf-8"),
            filename=f"daily_result_{date_from}.html",
        )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001
    """Print the received data and remove the button."""
    user = get_user_if_can_access(update.message.from_user)
    form_data = json.loads(update.effective_message.web_app_data.data)

    save_daily_data(user, **form_data)

    await update.message.reply_markdown_v2(
        text=DAILY_DATA_SAVE_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )


async def add_user_to_allow_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = get_user_if_can_access(update.message.from_user)

    if not user or not user.is_admin:
        await update.message.reply_text(
            text=NOT_ALLOWED_MESSAGE,
        )
        return

    user_id_to_add: int = context.args[0]

    add_user_id_to_allow_access(user_id_to_add)

    await update.effective_message.reply_text(
        text=ALLOW_ID_ADDED_SUCCESSFUL % user_id_to_add,
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    await update.effective_message.reply_text(text=UNHANDLED_ERROR, reply_markup=ReplyKeyboardRemove())


def add_handlers(application: Application) -> Application:
    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(help_command, pattern="^" + str(HELP) + "$"),
                CallbackQueryHandler(daily_command, pattern="^" + str(DAILY) + "$"),
                CallbackQueryHandler(id_command, pattern="^" + str(ID) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(END) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("report", get_daily_result))
    application.add_handler(CommandHandler("allow_access", add_user_to_allow_list))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.add_error_handler(error_handler)

    return application
