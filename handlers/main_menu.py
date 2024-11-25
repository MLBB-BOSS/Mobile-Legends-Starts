# UTC:22:00
# 2024-11-25
# handlers/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu message handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Received /start from user {message.from_user.id}")
    await message.answer(
        "Вітаю в MLS Bot! 🎮\n"
        "Ваш помічник у світі Mobile Legends!\n"
        "Оберіть опцію з меню нижче:",
        reply_markup=get_main_keyboard()
    )
