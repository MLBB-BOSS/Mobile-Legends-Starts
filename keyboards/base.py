# File: keyboards/main_menu.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class MainMenu(BaseKeyboard):
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        """Main menu keyboard"""
        buttons = [
            "buttons.navigation",
            "buttons.profile",
            "buttons.settings",
            "buttons.help"
        ]
        return cls.create_keyboard(buttons, row_width=2, add_back=False)
