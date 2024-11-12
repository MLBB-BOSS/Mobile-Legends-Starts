# core/info_handler.py

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"Вітаю, {user.first_name}! Ласкаво просимо до бота Mobile Legends!"
    
    # Головне меню з кнопками
    keyboard = [
        [InlineKeyboardButton("Інформація про героїв", callback_data='heroes_info')],
        [InlineKeyboardButton("Завантажити скріншот", callback_data='upload_screenshot')],
        [InlineKeyboardButton("Мій профіль", callback_data='view_profile')],
        [InlineKeyboardButton("Лідерборд", callback_data='leaderboard')],
        [InlineKeyboardButton("Допомога", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    logger.info(f"User {user.username or user.id} started the bot.")

async def get_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Функція для повторного відправлення головного меню
    keyboard = [
        [InlineKeyboardButton("Інформація про героїв", callback_data='heroes_info')],
        [InlineKeyboardButton("Завантажити скріншот", callback_data='upload_screenshot')],
        [InlineKeyboardButton("Мій профіль", callback_data='view_profile')],
        [InlineKeyboardButton("Лідерборд", callback_data='leaderboard')],
        [InlineKeyboardButton("Допомога", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Оберіть опцію:", reply_markup=reply_markup)
    logger.info("Main menu sent to user.")
