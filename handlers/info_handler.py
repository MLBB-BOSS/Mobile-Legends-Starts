# handlers/info_handler.py
from aiogram import F, Router
from aiogram.types import Message

info_router = Router()

@info_router.message(F.text == "/info")
async def info_command(message: Message):
    await message.reply("Це загальна інформація про бота Mobile Legends.")
