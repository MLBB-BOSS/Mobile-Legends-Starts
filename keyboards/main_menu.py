# keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("🧭 Навігація"), KeyboardButton("🪪 Профіль")]
            ],
            resize_keyboard=True
        )
