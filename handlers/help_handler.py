# handlers/help_handler.py

from aiogram import Router
from aiogram.types import Message

help_router = Router()

@help_router.message(commands=["help"])
async def help_command(message: Message):
    await message.reply("📖 Допомога\n\n"
                        "/start - Запустити бота\n"
                        "/help - Отримати допомогу\n"
                        "/screenshots - Переглянути скріншоти\n"
                        "/leaderboard - Таблиця лідерів\n"
                        "/profile - Ваш профіль")
