# core/help_handler.py

from telegram import Update
from telegram.ext import CallbackContext

def handle_help(update: Update, context: CallbackContext):
    help_text = (
        "🔹 **Доступні команди та функції:**\n"
        "/start - Початок роботи з ботом\n"
        "/profile - Переглянути свій профіль\n"
        "/leaderboard - Переглянути лідерборд\n"
        "Також ви можете використовувати кнопки нижче для навігації."
    )
    update.message.reply_text(help_text, parse_mode='Markdown')
