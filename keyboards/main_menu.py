# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import get_message as _

class MainMenu:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=_("buttons.navigation")),
                    KeyboardButton(text=_("buttons.profile"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
