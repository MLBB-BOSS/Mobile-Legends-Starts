# core/leaderboard_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def view_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Логіка для відображення лідерборду
    leaderboard_info = "🏆 **Лідерборд:**\n\n1. @user1 - 150 балів\n2. @user2 - 120 балів\n3. @user3 - 100 балів"
    
    await update.message.reply_text(leaderboard_info, parse_mode='Markdown')
    logger.info("Leaderboard viewed by user.")
