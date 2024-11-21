# File: keyboards/navigation.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class NavigationKeyboard(BaseKeyboard):
    @classmethod
    def main_menu(cls) -> ReplyKeyboardMarkup:
        """Main navigation menu"""
        buttons = [
            "buttons.navigation.main.team",
            "buttons.navigation.main.tournaments",
            "buttons.navigation.main.rating",
            "buttons.navigation.main.screenshots",
            "buttons.navigation.main.achievements",
            "buttons.navigation.main.notes"
        ]
        return cls.create_keyboard(buttons, row_width=3, add_back=False)

    @classmethod
    def heroes_menu(cls) -> ReplyKeyboardMarkup:
        """Heroes selection menu"""
        buttons = [
            "buttons.navigation.heroes.tank",
            "buttons.navigation.heroes.fighter", 
            "buttons.navigation.heroes.assassin",
            "buttons.navigation.heroes.mage",
            "buttons.navigation.heroes.marksman",
            "buttons.navigation.heroes.support"
        ]
        return cls.create_keyboard(buttons, row_width=3)
