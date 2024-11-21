from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from utils import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def unhandled_message(message: Message):
    logger.info(f"Отримано необроблене повідомлення: {message.text}")
    try:
        # Передаємо 'message' як аргумент для форматування
        response_text = loc.get_message("messages.unhandled_message", message=message.text)
        await message.answer(
            response_text,
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відправці повідомлення: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
