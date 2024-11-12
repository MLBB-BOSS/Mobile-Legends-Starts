# core/callback_handler.py

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from core.info_handler import get_main_menu
from core.profile_handler import view_profile
from core.leaderboard_handler import view_leaderboard
from core.heroes_info_handler import handle_heroes_info
from core.help_handler import handle_help
from core.screenshot_handler import handle_screenshot

logger = logging.getLogger(__name__)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Відповідь на callback query

    data = query.data
    user = update.effective_user

    logger.info(f"User {user.username or user.id} clicked button with data: {data}")

    if data == 'heroes_info':
        await handle_heroes_info(update, context)
    elif data == 'upload_screenshot':
        # Відправка повідомлення про завантаження скріншоту
        await query.message.reply_text("Будь ласка, завантажте скріншот гри.")
    elif data == 'view_profile':
        await view_profile(update, context)
    elif data == 'leaderboard':
        await view_leaderboard(update, context)
    elif data == 'help':
        await handle_help(update, context)
    else:
        await query.message.reply_text("Неопізнана команда.")
        logger.warning(f"Unrecognized callback data: {data}")
