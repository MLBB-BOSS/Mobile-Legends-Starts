# File: keyboards/profile.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class ProfileKeyboard(BaseKeyboard):
    @classmethod
    def main_menu(cls) -> ReplyKeyboardMarkup:
        """Profile main menu"""
        buttons = [
            "buttons.profile.info",
            "buttons.profile.statistics",
            "buttons.profile.badges",
            "buttons.profile.favorites",
            "buttons.profile.gallery",
            "buttons.profile.update"
        ]
        return cls.create_keyboard(buttons, row_width=3)
