# File: keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup
from keyboards.base import BaseKeyboard

class NavigationMenu(BaseKeyboard):
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            "buttons.guides",
            "buttons.characters",
            "buttons.counter_picks",
            "buttons.builds",
            "buttons.voting"
        ]
        return cls.create_keyboard(
            buttons, 
            row_width=2,
            back_key="buttons.back_to_navigation"
        )
