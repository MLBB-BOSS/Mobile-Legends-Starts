from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import MainMenu
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_command(message: types.Message):
    try:
        keyboard = MainMenu.get_main_menu()
        await message.answer(
            "Вітаю! Оберіть розділ:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при старті: {e}")
        await message.answer("Вибачте, сталася помилка.")
