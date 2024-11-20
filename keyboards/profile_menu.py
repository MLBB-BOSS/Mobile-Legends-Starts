# File: keyboards/profile_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class ProfileMenu:
    @staticmethod
    def get_profile_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            KeyboardButton(text=loc.get_message("buttons.statistics")),
            KeyboardButton(text=loc.get_message("buttons.achievements"))
        )
        keyboard.add(
            KeyboardButton(text=loc.get_message("buttons.back"))
        )
        return keyboard
