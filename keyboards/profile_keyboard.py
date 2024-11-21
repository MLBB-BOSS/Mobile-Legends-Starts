# File: keyboards/profile_keyboard.py
from .base_keyboard import BaseKeyboard

class ProfileKeyboard(BaseKeyboard):
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "📊 Статистика",
            "🏆 Досягнення",
            "⚙️ Налаштування",
            "📝 Зворотний зв'язок",
            "❓ Допомога",
            "🔙 Назад до Головного меню"
        ]
        return self.create_markup(buttons, row_width=2)

    # Add other profile submenus...
