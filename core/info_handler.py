# core/info_handler.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def get_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Створення кнопок для головного меню
        keyboard = [
            [InlineKeyboardButton("Інформація про героїв", callback_data='info_heroes')],
            [InlineKeyboardButton("Завантажити скріншот", callback_data='upload_screenshot')],
            [InlineKeyboardButton("Мій профіль", callback_data='view_profile')],
            [InlineKeyboardButton("Лідерборд", callback_data='view_leaderboard')],
            [InlineKeyboardButton("Допомога", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Відправлення повідомлення з меню
        await update.message.reply_text('Вітаю! Виберіть опцію:', reply_markup=reply_markup)
        logger.info(f"Displayed main menu to user {update.effective_user.username}")
    except Exception as e:
        logger.error(f"Error in get_main_menu: {e}")
        await update.message.reply_text("Виникла помилка при відображенні меню.")
