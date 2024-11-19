from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc  # Змінений імпорт

class NavigationMenu:
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.guides")),
                    KeyboardButton(text=loc.get_message("buttons.characters"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.counter_picks")),
                    KeyboardButton(text=loc.get_message("buttons.builds"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.voting")),
                    KeyboardButton(text=loc.get_message("buttons.back"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
