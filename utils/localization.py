Аfrom utils.localization_instance import loc
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
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
                    KeyboardButton(text=loc.get_message("buttons.back"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    # Existing methods...

    def get_builds_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.build1")),
                    KeyboardButton(text=loc.get_message("buttons.build2"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard 
