# core/profile_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from models.contribution import Contribution

logger = logging.getLogger(__name__)

async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        contributions = Contribution.get_user_contributions(user.id)  # Метод для отримання внесків користувача
        total_points = sum(c.points for c in contributions)
        badges = Contribution.get_user_badges(user.id)  # Метод для отримання бейджів користувача

        profile_info = f"📄 **Ваш профіль:**\n\n"
        profile_info += f"👤 **Ім'я:** {user.first_name} {user.last_name if user.last_name else ''}\n"
        profile_info += f"🔢 **ID:** {user.id}\n"
        profile_info += f"⭐ **Бали:** {total_points}\n"
        profile_info += f"🏅 **Бейджі:** {', '.join(badges) if badges else 'Немає'}"

        await update.message.reply_text(profile_info, parse_mode='Markdown')
        logger.info(f"User {user.username or user.id} viewed their profile.")
    except Exception as e:
        logger.error(f"Error in view_profile: {e}")
        await update.message.reply_text("Виникла помилка при відображенні профілю.")
