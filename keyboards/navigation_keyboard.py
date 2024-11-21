# keyboards/navigation_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard

class NavigationKeyboard(BaseKeyboard):
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["👥 Персонажі", "🗺 Мапи"],
            ["🏆 Турніри", "📖 Гайди"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)
