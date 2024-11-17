# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text=loc.get_message("buttons.guides")),
                KeyboardButton(text=loc.get_message("buttons.profile"))
            ],
            [
                KeyboardButton(text=loc.get_message("buttons.voting")),
                KeyboardButton(text=loc.get_message("buttons.characters"))
            ]
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
