# UTC:21:40
# 2024-11-24
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.
# keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Головне меню
    """
    logger.info("Creating main keyboard with buttons: 🧭 Навігація, 🛡️ Профіль")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🛡️ Профіль")]
        ],
        resize_keyboard=True
    )
    return keyboard
