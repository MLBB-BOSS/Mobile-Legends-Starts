# File: keyboards/profile.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class ProfileKeyboard(BaseKeyboard):
    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        """Profile menu keyboard"""
        buttons = [
            "buttons.statistics",
            "buttons.achievements",
            "buttons.feedback"
        ]
        return cls.create_keyboard(buttons, row_width=3)
