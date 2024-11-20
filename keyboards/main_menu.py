# File: keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            KeyboardButton(text=loc.get_message("buttons.navigation")),
            KeyboardButton(text=loc.get_message("buttons.profile"))
        )
        return keyboard
