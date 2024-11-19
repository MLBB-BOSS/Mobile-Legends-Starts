# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class MainMenu:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.navigation")),
                    KeyboardButton(text=loc.get_message("buttons.profile"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
