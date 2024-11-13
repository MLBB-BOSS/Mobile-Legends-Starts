# core/profile_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp
from services.screenshot_service import get_user_profile

@dp.message_handler(Command("profile"))
async def send_profile(message: types.Message):
    profile = await get_user_profile(message.from_user.id)
    await message.reply(profile, parse_mode="HTML")
