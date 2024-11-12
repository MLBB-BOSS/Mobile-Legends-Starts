# main.py

from core.info_handler import start, get_main_menu
from core.profile_handler import view_profile
from core.screenshot_handler import handle_screenshot
from core.leaderboard_handler import view_leaderboard
from core.heroes_info_handler import handle_heroes_info
from core.help_handler import handle_help
from core.callback_handler import handle_callback
from config.settings import TELEGRAM_BOT_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Додавання обробників команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", view_profile))
    app.add_handler(CommandHandler("leaderboard", view_leaderboard))
    app.add_handler(CommandHandler("heroes", handle_heroes_info))
    app.add_handler(CommandHandler("help", handle_help))
    
    # Обробка завантажених фото
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    
    # Обробка callback queries (наприклад, кнопок)
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Запуск бота
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
