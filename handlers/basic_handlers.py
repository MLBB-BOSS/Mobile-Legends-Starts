# handlers/basic_handlers.py

from aiogram import Router, types
from aiogram.types import Message

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    """Відправляє привітальне повідомлення при запуску команди /start."""
    await message.reply("Вітаю! Я ваш бот, готовий допомогти.")
