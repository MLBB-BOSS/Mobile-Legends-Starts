# main.py

from core import (
    start,
    get_main_menu,
    handle_screenshot,
    view_profile,
    view_leaderboard,
    handle_heroes_info,
    handle_help,
    handle_callback,
    handle_settings
)
from config.settings import TELEGRAM_BOT_TOKEN
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
import logging
import asyncio

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додавання обробників команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", view_profile))
    app.add_handler(CommandHandler("leaderboard", view_leaderboard))
    app.add_handler(CommandHandler("heroes", handle_heroes_info))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("settings", handle_settings))

    # Обробка завантажених фото
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    # Обробка текстових повідомлень
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_callback))

    # Обробка callback queries (натискання кнопок)
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Запуск бота
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
