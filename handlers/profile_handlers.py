# handlers/profile_handlers.py
# UTC:22:00
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers for profile menu and user-related actions
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import get_profile_keyboard
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🔙 Назад")
async def back_to_main_from_profile(message: Message):
    logger.info(f"User {message.from_user.id} returned to main menu from profile")
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )
