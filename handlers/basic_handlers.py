# handlers/basic_handlers.py

from aiogram import Router
from aiogram.types import Message

basic_router = Router()

@basic_router.message(commands=["start"])
async def start_command(message: Message):
    await message.reply("Вітаю! Я ваш бот, готовий допомогти.")

@basic_router.message(commands=["help"])
async def help_command(message: Message):
    await message.reply("📖 Допомога\n\n"
                        "/start - Запустити бота\n"
                        "/help - Отримати допомогу\n"
                        "/screenshots - Переглянути скріншоти\n"
                        "/leaderboard - Таблиця лідерів\n"
                        "/profile - Ваш профіль")
