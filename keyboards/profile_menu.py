# UTC:21:40
# 2024-11-24
# keyboards/profile_menu.py
# Author: MLBB-BOSS
# Description: Profile menu keyboard layouts
# The era of artificial intelligence.
# keyboards/profile_menu.py
# keyboards/profile_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    """Підменю Профіль"""
    logger.info("Creating profile keyboard with buttons: 📈 Статистика, 🏆 Досягнення, ⚙️ Налаштування, 💌 Зворотний Зв'язок, ❓ Допомога, 🔙 Назад до Головного")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Статистика"), KeyboardButton(text="🏆 Досягнення")],
            [KeyboardButton(text="⚙️ Налаштування"), KeyboardButton(text="💌 Зворотний Зв'язок")],
            [KeyboardButton(text="❓ Допомога"), KeyboardButton(text="🔙 Назад до Головного")]
        ],
        resize_keyboard=True
    )
    return keyboard
