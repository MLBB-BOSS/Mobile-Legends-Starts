from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Профіль")
async def handle_profile(message: Message):
    await message.reply("Це ваш профіль.")
