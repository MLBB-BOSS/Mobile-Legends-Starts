from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    @staticmethod
    def get_navigation_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛡️ Персонажі"), KeyboardButton(text="📚 Гайди")],
                [KeyboardButton(text="⚔️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
                [KeyboardButton(text="🔙 Назад")]
            ],
            resize_keyboard=True
        )
