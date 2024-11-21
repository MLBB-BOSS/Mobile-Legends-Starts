# handlers/error_handler.py
from aiogram import Router, F
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text)
async def handle_unknown_message(message: Message):
    logger.info(f"Отримано необроблене повідомлення: {message.text}")
    await message.answer(
        "Вибачте, я не розумію цю команду. Використовуйте кнопки меню."
    )
