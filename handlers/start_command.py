from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import MainMenu
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_command(message: types.Message):
    try:
        keyboard = MainMenu.get_main_menu()
        await message.answer(
            loc.get_message("messages.start_command"),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при старті: {e}")
        await message.answer(loc.get_message("messages.error"))
