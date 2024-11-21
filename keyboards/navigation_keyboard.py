from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.keyboard_buttons import Buttons

class NavigationKeyboard:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(str(Buttons.NAVIGATION)), KeyboardButton(str(Buttons.HEROES))],
            [KeyboardButton(str(Buttons.PROFILE)), KeyboardButton(str(Buttons.SETTINGS))]
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
