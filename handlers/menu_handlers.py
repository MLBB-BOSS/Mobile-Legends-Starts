# handlers/menu_handlers.py

import logging
from aiogram import Router, types
from aiogram.filters import StringFilter as F Text  # Альтернатива
from utils.localization import loc
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu

logger = logging.getLogger(__name__)
router = Router()

@router.message(Text(equals=loc.get_message("buttons.show_heroes")))
async def show_heroes(message: types.Message):
    try:
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=HeroMenu().get_hero_classes_menu()
        )
        logger.info(f"Користувач {message.from_user.id} запитав показати героїв.")
    except Exception as e:
        logger.exception(f"Помилка в show_heroes хендлері: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
