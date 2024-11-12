# core/profile_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # Логіка для відображення профілю користувача
    profile_info = f"📄 **Ваш профіль:**\n\n"
    profile_info += f"👤 **Ім'я:** {user.first_name} {user.last_name if user.last_name else ''}\n"
    profile_info += f"🔢 **ID:** {user.id}\n"
    # Додайте іншу необхідну інформацію
    await update.message.reply_text(profile_info, parse_mode='Markdown')
    logger.info(f"User {user.username or user.id} viewed their profile.")
