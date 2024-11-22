# keyboards/navigation_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    @staticmethod
    def get_main_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Мій профіль")],
                [KeyboardButton(text="ℹ️ Допомога")],
            ],
            resize_keyboard=True
        )
