# main.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.handlers import main_menu
from core.config import settings
from core.logging import setup_logging

# Налаштування логування
setup_logging()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я MLSnap бот. Як я можу допомогти?")

def main():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Додавання обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(main_menu.router)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
