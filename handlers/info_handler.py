# handlers/info_handler.py

from aiogram import Router
from aiogram.types import Message

info_router = Router()

@info_router.message(commands=["info"])
async def info_command(message: Message):
    await message.reply("Це загальна інформація!")
