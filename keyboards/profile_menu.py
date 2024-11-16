# File: keyboards/profile_menu.py
from .base import BaseKeyboard

class ProfileMenu(BaseKeyboard):
    """Меню особистого кабінету"""
    
    @classmethod
    def get_profile_menu(cls):
        """Повертає меню особистого кабінету"""
        buttons = [
            [{"text": "📊 Статистика", "callback_data": "statistics"}],
            [{"text": "🏅 Мої Досягнення", "callback_data": "achievements"}],
            [{"text": "⚙️ Налаштування", "callback_data": "settings"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_main"}]
        ]
        return cls.create_keyboard(buttons, is_inline=True)
