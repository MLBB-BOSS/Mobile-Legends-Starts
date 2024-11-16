# File: keyboards/main_menu.py
from .base import BaseKeyboard

class MainMenu(BaseKeyboard):
    """Головне меню бота"""
    
    @classmethod
    def get_main_menu(cls):
        """Повертає головне меню з двома основними кнопками"""
        buttons = [
            "🧭 Навігація",
            "🪪 Мій Кабінет"  # Переконайтесь, що текст точно співпадає
        ]
        return cls.create_keyboard(buttons, row_width=2)
