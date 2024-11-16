from .base import BaseKeyboard

class NavigationMenu(BaseKeyboard):
    """Меню навігації"""
    
    @classmethod
    def get_navigation_menu(cls) -> InlineKeyboardMarkup:
        """Повертає меню навігації"""
        buttons = [
            [{"text": "📚 Гайди", "callback_data": "guides"}],
            [{"text": "🧙‍♂️ Персонажі", "callback_data": "heroes"}],
            [{"text": "🎯 Контр-Піки", "callback_data": "counter_picks"}],
            [{"text": "⚔️ Збірки", "callback_data": "builds"}],
            [{"text": "🗳 Голосування", "callback_data": "voting"}],
            [{"text": "🔙 Назад", "callback_data": "back_to_main"}]
        ]
        return cls.create_keyboard(buttons, is_inline=True)
