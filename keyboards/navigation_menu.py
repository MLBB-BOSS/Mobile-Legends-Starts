from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import get_message as _

class NavigationMenu:
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=_("buttons.guides")),
                    KeyboardButton(text=_("buttons.characters"))
                ],
                [
                    KeyboardButton(text=_("buttons.counter_picks")),
                    KeyboardButton(text=_("buttons.builds"))
                ],
                [
                    KeyboardButton(text=_("buttons.voting")),
                    KeyboardButton(text=_("buttons.back"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
