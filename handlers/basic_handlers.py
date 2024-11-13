# handlers/basic_handlers.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp

@dp.message_handler(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = (
        "👋 <b>Вітаємо!</b>\n\n"
        "Цей бот допоможе вам з інформацією про героїв та керування скріншотами."
    )
    await message.reply(welcome_text, parse_mode="HTML")
