from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Навігація")
async def handle_navigation(message: Message):
    await message.reply("Це розділ навігації.")
