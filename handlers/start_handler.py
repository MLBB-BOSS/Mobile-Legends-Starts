# handlers/start_handler.py

from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.reply("Вітаю! Я ваш бот, готовий допомогти.")
