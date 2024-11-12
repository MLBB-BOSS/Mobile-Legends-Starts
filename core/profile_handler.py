# core/profile_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # Тут додайте логіку для відображення профілю користувача
    await update.message.reply_text(f"Ваш профіль, {user.first_name}!")
    logger.info(f"User {user.username} viewed their profile.")
