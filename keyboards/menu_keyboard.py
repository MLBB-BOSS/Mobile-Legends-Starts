# keyboards/menu_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class MenuKeyboard:
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="🧭 Навігація", callback_data="menu_navigation")],
            [InlineKeyboardButton(text="🪪 Профіль", callback_data="menu_profile")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
