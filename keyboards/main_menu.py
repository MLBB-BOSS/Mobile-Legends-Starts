# UTC:21:40
# 2024-11-24
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.

import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logger = logging.getLogger(__name__)

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Головне меню
    """
    logger.info(f"KeyboardButton class: {KeyboardButton}")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🧭 Навігація"), KeyboardButton("🛡️ Профіль")]],
        resize_keyboard=True
    )
    return keyboard
