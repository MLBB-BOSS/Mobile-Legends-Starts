# File: keyboards/navigation.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class NavigationKeyboard(BaseKeyboard):
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        """Navigation menu keyboard"""
        buttons = [
            "buttons.guides",
            "buttons.characters",
            "buttons.counter_picks",
            "buttons.builds",
            "buttons.voting"
        ]
        return cls.create_keyboard(
            buttons, 
            row_width=3,
            back_key="buttons.back"
        )
