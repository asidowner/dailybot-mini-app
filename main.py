"""
Simple example of a Telegram WebApp which displays a color picker.
The static website for this website is hosted by the PTB team for your convenience.
Currently only showcases starting the WebApp via a KeyboardButton, as all other methods would
require a bot token.
"""
import logging

import sentry_sdk
from telegram import Update
from telegram.ext import Application

from core.config import settings

from bot.handlers import add_handlers
from bot.jobs import add_jobs
from bot.services.user import add_user_id_to_allow_access

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start project. Configure sentry and start bot."""
    if settings.sentry_dsn:
        # Start sentry
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )

    # Create the Application and pass it your bot's token.
    application = Application.builder().concurrent_updates(concurrent_updates=False).token(settings.bot_token).build()

    for user_id in settings.admin_user_ids:
        add_user_id_to_allow_access(user_id)

    add_handlers(application)
    add_jobs(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
