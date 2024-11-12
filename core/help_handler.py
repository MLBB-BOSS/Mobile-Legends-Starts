# core/help_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

HELP_TEXT = """
📚 **Допомога:**

- `/start` - Початок взаємодії з ботом та відображення головного меню.
- `Інформація про героїв` - Отримати інформацію про доступних героїв.
- `Завантажити скріншот` - Завантажити скріншот гри та отримати бали.
- `Мій профіль` - Переглянути свій профіль та бали.
- `Лідерборд` - Переглянути топ користувачів.
- `Допомога` - Отримати цю допомогу.

Якщо у вас є питання або пропозиції, звертайтесь до адміністраторів.
"""

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(HELP_TEXT, parse_mode='Markdown')
        logger.info("Help information sent to user.")
    except Exception as e:
        logger.error(f"Error in handle_help: {e}")
        await update.message.reply_text("Виникла помилка при відображенні допомоги.")
