from telegram.ext import (
    Application,
    CommandHandler,
)
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
    ChatJoinRequestHandler,
)
from config.config import TELEGRAM_TOKEN
from bot.handlers.start_handler import start, button_handler

from logs.logger import logger


def init_bot():
    persistence = PicklePersistence("bot_cache")
    application = (
        Application.builder().token(TELEGRAM_TOKEN).persistence(persistence).build()
    )
    logger.info("Бот полетел🤟")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={},
        fallbacks=[CommandHandler("start", start)],
        name="mian_conversation",
        persistent=True,
    )
    application.add_handler(conv_handler)

    application.add_handler(CallbackQueryHandler(button_handler))
    return application
