# handlers/start_command.py

import logging

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у start_command.py")

from aiogram import Router, types
from aiogram.filters import Command  # Коректний імпорт
from utils.localization import loc
from keyboards.main_menu import MainMenu

logger.debug("Імпорти виконано успішно у start_command.py")

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            loc.get_message("messages.welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
        logger.info(f"Користувач {message.from_user.id} почав роботу з ботом.")
    except Exception as e:
        logger.exception(f"Помилка в хендлері команди /start: {e}")
        await message.answer(
            loc.get_message("messages.errors.general")
        )
