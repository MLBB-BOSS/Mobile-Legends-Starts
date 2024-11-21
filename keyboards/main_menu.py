from aiogram.types import InlineKeyboardButton
from .base_keyboard import BaseKeyboard

class MainMenuKeyboard(BaseKeyboard):
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="🧭 Навігація", callback_data="menu_navigation")],
            [InlineKeyboardButton(text="🪪 Профіль", callback_data="menu_profile")],
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
