# keyboards/navigation_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard
from keyboards.keyboard_buttons import Buttons

class NavigationKeyboard(BaseKeyboard):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [Buttons.NAVIGATION, Buttons.HEROES],
            [Buttons.PROFILE, Buttons.SETTINGS]
        ]
        return self.create_keyboard(buttons)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [Buttons.CHARACTERS, Buttons.MAPS],
            [Buttons.TOURNAMENTS, Buttons.GUIDES],
            [Buttons.MAIN_MENU]
        ]
        return self.create_keyboard(buttons)
