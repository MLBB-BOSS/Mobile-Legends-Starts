# handlers/profile_handler.py
from aiogram import F, Router
from aiogram.types import Message

profile_router = Router()

@profile_router.message(F.text == "/profile")
async def profile_command(message: Message):
    await message.reply("Ваш профіль: інформація буде додана.")
