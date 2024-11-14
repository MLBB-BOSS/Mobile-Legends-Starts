# handlers/screenshot_handler.py

from aiogram import Router
from aiogram.types import Message
from services.screenshot_service import get_hero_info

screenshot_router = Router()

@screenshot_router.message(commands=["screenshots"])
async def screenshots_command(message: Message):
    hero_info = get_hero_info()
    await message.reply(f"Скріншоти: {hero_info}")
