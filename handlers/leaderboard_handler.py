# handlers/leaderboard_handler.py
from aiogram import F, Router
from aiogram.types import Message

leaderboard_router = Router()

@leaderboard_router.message(F.text == "/leaderboard")
async def leaderboard_command(message: Message):
    await message.reply("Тут буде таблиця лідерів.")
