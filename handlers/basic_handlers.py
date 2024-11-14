# handlers/basic_handlers.py
from aiogram import F, Router
from aiogram.types import Message

start_router = Router()

@start_router.message(F.text == "/start")
async def start_command(message: Message):
    """Відповідає на команду /start."""
    await message.reply("Ласкаво просимо до бота Mobile Legends!")
