# File: handlers/profile_handlers.py

import logging
from aiogram import Router, F, types
from keyboards.profile_keyboard import ProfileKeyboard
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🪪 Профіль")
async def show_profile_menu(message: types.Message):
    """Handle profile menu"""
    try:
        keyboard = ProfileKeyboard()
        await message.answer(
            text=loc.get_message("profile_menu"),
            reply_markup=keyboard.get_profile_menu()
        )
        logger.debug(f"Profile menu shown to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error showing profile menu: {e}")
        await message.answer(loc.get_message("error.general"))

# Add handlers for profile submenus (Statistics, Achievements, etc.)
