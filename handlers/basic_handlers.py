from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /start"""
    await update.message.reply_text(
        "Привіт! Я MLBB-BOSS Telegram Bot. "
        "Використовуй /help для отримання списку команд."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /help"""
    help_text = """
    Доступні команди:
    /start - Почати роботу з ботом
    /help - Показати це повідомлення
    """
    await update.message.reply_text(help_text)
