# keyboards/navigation_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard
from keyboards.keyboard_buttons import Buttons

class NavigationKeyboard(BaseKeyboard):
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [Buttons.CHARACTERS, Buttons.MAPS],
            [Buttons.TOURNAMENTS, Buttons.GUIDES],
            [Buttons.BACK_TO_MAIN]
        ]
        return self.create_reply_markup(keyboard)

    def get_characters_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["🛡️ Танк", "🔮 Маг", "🏹 Стрілець"],
            ["🗡️ Асасін", "🛠️ Підтримка"],
            [Buttons.BACK_TO_MAIN]
        ]
        return self.create_reply_markup(keyboard)
