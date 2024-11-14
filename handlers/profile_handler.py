# handlers/profile_handler.py

from aiogram import Router
from aiogram.types import Message

profile_router = Router()

@profile_router.message(commands=["profile"])
async def profile_command(message: Message):
    await message.reply("Ваш профіль!")
