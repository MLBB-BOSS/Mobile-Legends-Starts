# File: keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup
from keyboards.base import BaseKeyboard

class MainMenu(BaseKeyboard):
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            "buttons.navigation",
            "buttons.profile",
            "buttons.settings",
            "buttons.help"
        ]
        return cls.create_keyboard(buttons, row_width=2, add_back=False)
