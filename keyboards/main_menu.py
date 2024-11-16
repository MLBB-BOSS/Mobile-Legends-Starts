from aiogram.types import ReplyKeyboardMarkup
from .base import BaseKeyboard

class MainMenu(BaseKeyboard):
    """Головне меню бота"""
    
    @classmethod
    def get_main_menu(cls) -> ReplyKeyboardMarkup:
        """Повертає головне меню з двома основними кнопками"""
        buttons = [
            ["🧭 Навігація", "🪧 Мій Кабінет"]
        ]
        return cls.create_keyboard(buttons)
