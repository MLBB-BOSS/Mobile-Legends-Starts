# core/heroes_info_handler.py

from telegram import Update
from telegram.ext import CallbackContext

def handle_heroes_info(update: Update, context: CallbackContext):
    # Отримання інформації про героїв
    heroes_info = "Ось інформація про героїв:\n\n1. Герой А - Опис...\n2. Герой Б - Опис..."
    update.message.reply_text(heroes_info)
