# keyboards/main_menu.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Клавіатури для головного меню

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MainMenuKeyboard:
    @staticmethod
    def get_keyboard() -> InlineKeyboardMarkup:
        """Створення клавіатури головного меню"""
        builder = InlineKeyboardBuilder()
        
        # Додавання кнопок
        builder.add(
            InlineKeyboardButton(text="🎮 Турніри", callback_data="tournaments"),
            InlineKeyboardButton(text="👤 Профіль", callback_data="profile"),
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="rating"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
            InlineKeyboardButton(text="ℹ️ Допомога", callback_data="help")
        )
        
        # Налаштування розміщення кнопок
        builder.adjust(2, 2, 1)
        return builder.as_markup()
