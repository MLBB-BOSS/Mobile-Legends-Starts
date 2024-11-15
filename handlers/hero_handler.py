# handlers/hero_handler.py

from aiogram import Router
from aiogram.filters.text import Text  # Правильний імпорт для aiogram 3.x  # Оновлений шлях імпорту
from aiogram.types import Message

router = Router()

@router.message(Text(equals="hero"))
async def handle_hero_message(message: Message):
    await message.reply("This is a hero response!")
