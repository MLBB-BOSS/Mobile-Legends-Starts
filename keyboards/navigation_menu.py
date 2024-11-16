# File: keyboards/navigation_menu.py
from .base import BaseKeyboard

class NavigationMenu(BaseKeyboard):
    """Меню навігації"""
    
    @classmethod
    def get_navigation_menu(cls):
        """Повертає меню навігації"""
        buttons = [
            "📚 Гайди",
            "🧙‍♂️ Персонажі",
            "🎯 Контр-Піки",
            "⚔️ Збірки",
            "🗳 Голосування",
            "🔙 Головне меню"
        ]
        return cls.create_keyboard(buttons, row_width=2)
