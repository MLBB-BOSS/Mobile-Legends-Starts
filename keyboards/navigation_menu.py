# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    @staticmethod
    def get_navigation_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🛡️ Персонажі"), KeyboardButton("📚 Гайди")],
                [KeyboardButton("⚔️ Контр-піки"), KeyboardButton("⚜️ Білди")],
                [KeyboardButton("📊 Голосування"), KeyboardButton("🔄 Назад")]
            ],
            resize_keyboard=True
        )
