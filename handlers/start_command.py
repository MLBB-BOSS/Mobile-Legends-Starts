from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_menu import MainMenu
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    try:
        keyboard = MainMenu.get_main_menu()
        await message.answer(
            "Ласкаво просимо до бота! Оберіть дію:",
            reply_markup=keyboard
        )
        logger.info("Main menu sent successfully.")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await message.answer("Сталася помилка при запуску бота.")
