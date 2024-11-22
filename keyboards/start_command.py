# keyboards/start_command.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StartMenu:
    """Клавіатура для стартового меню"""
    @staticmethod
    def get_start_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Профіль")],
                [KeyboardButton(text="❓ Допомога")],
            ],
            resize_keyboard=True
        )
