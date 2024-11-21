# keyboards/main_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard

class MainKeyboard(BaseKeyboard):
    """Class for main keyboard functionalities"""

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["🧭 Навігація", "🎯 Герої"],
            ["🪪 Профіль", "⚙️ Налаштування"],
            ["🎫 Купити білети", "📊 Статистика"]
        ]
        return self.create_reply_markup(keyboard)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["👥 Персонажі", "🗺 Мапи"],
            ["🏆 Турніри", "📖 Гайди"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    # Інші методи...
