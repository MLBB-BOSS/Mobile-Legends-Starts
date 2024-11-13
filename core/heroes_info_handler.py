# core/heroes_info_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp
from services.screenshot_service import get_hero_info

@dp.message_handler(Command("heroes"))
async def send_heroes_info(message: types.Message):
    hero_info = await get_hero_info()
    await message.reply(hero_info, parse_mode="HTML")
