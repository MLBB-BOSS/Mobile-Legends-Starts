# UTC:21:40
# 2024-11-24
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.
# keyboards/navigation_menu.py
# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    """Підменю Навігація"""
    logger.info("Creating navigation keyboard with buttons: 🛡️ Персонажі, 📚 Гайди, ⚖️ Контр-піки, ⚜️ Білди, 📊 Голосування, 🔙 Назад")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡️ Персонажі"), KeyboardButton(text="📚 Гайди")],
            [KeyboardButton(text="⚖️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
            [KeyboardButton(text="📊 Голосування"), KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard
