from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/help")
async def help_handler(message: Message):
    await message.answer("Це довідка.")
