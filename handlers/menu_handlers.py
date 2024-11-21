# File: handlers/menu_handlers.py

import logging
from aiogram import Router, F, types
from keyboards.main_keyboard import MainKeyboard
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🔙 Назад до Головного меню")
async def return_to_main_menu(message: types.Message):
    """Handle return to main menu"""
    try:
        keyboard = MainKeyboard()
        await message.answer(
            text=loc.get_message("main_menu"),
            reply_markup=keyboard.get_main_menu()
        )
        logger.debug(f"User {message.from_user.id} returned to main menu")
    except Exception as e:
        logger.error(f"Error returning to main menu: {e}")
        await message.answer(loc.get_message("error.general"))
