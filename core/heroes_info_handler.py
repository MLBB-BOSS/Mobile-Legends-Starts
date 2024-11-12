# core/heroes_info_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# Приклад інформації про героїв. Можна замінити на динамічні дані з API або бази даних.
HEROES_INFO = {
    "Alucard": "🗡 **Alucard** - ближній бій, високий урон.",
    "Eudora": "⚡ **Eudora** - маг, сильний у контролі.",
    "Layla": "🔫 **Layla** - стрілець, дальній урон.",
    # Додайте більше героїв за потребою
}

async def handle_heroes_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        heroes_list = "\n".join([info for info in HEROES_INFO.values()])
        message = f"📜 **Інформація про героїв:**\n\n{heroes_list}"
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info("Heroes information viewed by user.")
    except Exception as e:
        logger.error(f"Error in handle_heroes_info: {e}")
        await update.message.reply_text("Виникла помилка при відображенні інформації про героїв.")
