# File: keyboards/profile_menu.py
from .base import BaseKeyboard

class ProfileMenu(BaseKeyboard):
    """Меню особистого кабінету"""
    
    @classmethod
    def get_profile_menu(cls):
        """Повертає меню особистого кабінету"""
        buttons = [
            ["📊 Статистика", "🏅 Досягнення"],
            ["⚙️ Налаштування"],
            ["🔙 Головне меню"]
        ]
        return cls.create_keyboard(buttons)
