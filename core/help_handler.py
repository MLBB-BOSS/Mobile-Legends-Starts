# core/help_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp

@dp.message_handler(Command("help"))
async def send_help(message: types.Message):
    help_text = (
        "📖 <b>Допомога</b>\n\n"
        "/start - Запустити бота\n"
        "/help - Отримати допомогу\n"
        "/screenshots - Переглянути скріншоти\n"
        "/leaderboard - Таблиця лідерів\n"
        "/profile - Ваш профіль"
    )
    await message.reply(help_text, parse_mode="HTML")
