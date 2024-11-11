# main.py

import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from core import (
    get_main_menu,
    handle_screenshot,
    view_profile,
    view_leaderboard,
    handle_heroes_info,
    handle_help,
    handle_callback
)
from config.settings import TELEGRAM_BOT_TOKEN, ENABLE_QUIZZES, ENABLE_NEWS
from services.database import init_db

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Ініціалізація бази даних
    init_db()
    
    # Створення Updater та Dispatcher
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Додавання обробника команди /start
    dispatcher.add_handler(CommandHandler('start', get_main_menu))
    logger.info("Added /start handler")

    # Додавання обробника для callback queries
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    logger.info("Added CallbackQueryHandler")

    # Додавання інших обробників за потребою
    if ENABLE_QUIZZES:
        from handlers.quizzes import handle_quiz
        dispatcher.add_handler(CommandHandler('quiz', handle_quiz))
        logger.info("Added /quiz handler")

    if ENABLE_NEWS:
        from handlers.news import handle_news
        dispatcher.add_handler(CommandHandler('news', handle_news))
        logger.info("Added /news handler")

    # Запуск бота
    updater.start_polling()
    logger.info("Bot started polling")
    updater.idle()
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
