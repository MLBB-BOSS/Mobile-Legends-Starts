# File: handlers/navigation_handlers.py

import logging
from aiogram import Router, F, types
from keyboards.navigation_keyboard import NavigationKeyboard
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: types.Message):
    """Handle navigation menu"""
    try:
        keyboard = NavigationKeyboard()
        await message.answer(
            text=loc.get_message("navigation_menu"),
            reply_markup=keyboard.get_navigation_menu()
        )
        logger.debug(f"Navigation menu shown to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error showing navigation menu: {e}")
        await message.answer(loc.get_message("error.general"))

@router.message(F.text == "👥 Персонажі")
async def show_heroes_menu(message: types.Message):
    """Handle heroes submenu"""
    try:
        keyboard = NavigationKeyboard()
        await message.answer(
            text=loc.get_message("heroes_menu"),
            reply_markup=keyboard.get_characters_menu()
        )
        logger.debug(f"Heroes menu shown to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error showing heroes menu: {e}")
        await message.answer(loc.get_message("error.general"))

# Add other navigation submenu handlers
