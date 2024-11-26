# /handlers/help.py
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/help")
async def help_handler(message: Message):
    """Обробник для команди /help"""
    await message.answer(
        "Це довідка. Сюди можна додати інформацію про використання бота."
    )
