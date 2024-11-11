# core/info_handler.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from config.settings import TELEGRAM_BOT_TOKEN

# Функція для обробки команди /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я ваш бот, що допомагає з Mobile Legends.")
    return

# Функція для основного меню
def get_main_menu():
    return [
        ["Персонажі", "Мета-білди"],
        ["Підтримка", "Зв'язок з нами"]
    ]

def main():
    from telegram.ext import Updater

    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
