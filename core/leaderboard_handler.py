# core/leaderboard_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from models.contribution import Contribution

logger = logging.getLogger(__name__)

async def view_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Отримання топ користувачів за балами
        top_users = Contribution.get_top_users(limit=10)  # Метод для отримання топ користувачів

        if not top_users:
            leaderboard_info = "Лідерборд порожній."
        else:
            leaderboard_info = "🏆 **Лідерборд:**\n\n"
            for idx, user in enumerate(top_users, start=1):
                leaderboard_info += f"{idx}. @{user.username or 'User' + str(user.user_id)} - {user.total_points} балів\n"

        await update.message.reply_text(leaderboard_info, parse_mode='Markdown')
        logger.info("Leaderboard viewed by user.")
    except Exception as e:
        logger.error(f"Error in view_leaderboard: {e}")
        await update.message.reply_text("Виникла помилка при відображенні лідерборду.")
