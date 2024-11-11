# core/callback_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

from core import (
    handle_heroes_info,
    handle_help,
    handle_screenshot_prompt,
    view_profile,
    view_leaderboard
)

logger = logging.getLogger(__name__)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    logger.info(f"Received callback data: {data}")

    if data == 'info_heroes':
        await handle_heroes_info(update, context)
    elif data == 'upload_screenshot':
        await handle_screenshot_prompt(update, context)
    elif data == 'view_profile':
        await view_profile(update, context)
    elif data == 'view_leaderboard':
        await view_leaderboard(update, context)
    elif data == 'help':
        await handle_help(update, context)
    else:
        await query.edit_message_text(text="Невідома опція.")
        logger.warning(f"Unknown callback data: {data}")
