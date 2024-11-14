# handlers/leaderboard_handler.py

from aiogram import Router
from aiogram.types import Message

leaderboard_router = Router()

@leaderboard_router.message(commands=["leaderboard"])
async def leaderboard_command(message: Message):
    await message.reply("Тут буде таблиця лідерів.")
