# keyboards/navigation_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard
from keyboards.keyboard_buttons import KeyboardButtons as kb

class NavigationKeyboard(BaseKeyboard):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [kb.NAVIGATION, kb.HEROES],
            [kb.PROFILE, kb.SETTINGS]
        ]
        return self.create_keyboard(buttons)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [kb.CHARACTERS, kb.MAPS],
            [kb.TOURNAMENTS, kb.GUIDES],
            [kb.MAIN_MENU]
        ]
        return self.create_keyboard(buttons)
