# handlers/heroes_info_handler.py

from aiogram import Router
from aiogram.types import Message

heroes_info_router = Router()

@heroes_info_router.message(commands=["hero_info"])
async def hero_info_command(message: Message):
    await message.reply("Інформація про героя!")
