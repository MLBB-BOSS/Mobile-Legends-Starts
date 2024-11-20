from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class NavigationMenu:
    @staticmethod
    def get_main_navigation() -> ReplyKeyboardMarkup:  # Перейменовуємо метод
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
