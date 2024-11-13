# leaderboard_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp
from services.screenshot_service import get_leaderboard

@dp.message_handler(Command("leaderboard"))
async def send_leaderboard(message: types.Message):
    leaderboard = await get_leaderboard()
    await message.reply(leaderboard, parse_mode="HTML")
