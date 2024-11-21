# File: keyboards/settings.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class SettingsKeyboard(BaseKeyboard):
    @classmethod
    def main_menu(cls) -> ReplyKeyboardMarkup:
        """Settings main menu"""
        buttons = [
            "buttons.settings.notifications",
            "buttons.settings.language",
            "buttons.settings.mode",
            "buttons.settings.interface",
            "buttons.settings.privacy",
            "buttons.settings.about"
        ]
        return cls.create_keyboard(buttons, row_width=3)
