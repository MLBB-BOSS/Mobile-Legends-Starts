# handlers/profile_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import get_profile_keyboard
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🪪 Профіль")
async def profile_menu(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Профіль'")
    await message.answer(
        "Ваш профіль:\nОберіть потрібний розділ:",
        reply_markup=get_profile_keyboard()
    )

@router.message(F.text == "🔙 Назад")
async def back_to_main_from_profile(message: Message):
    logger.info(f"User {message.from_user.id} returned to main menu from profile")
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )
