# File: utils/localization.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="buttons.guides"),
                    KeyboardButton(text="buttons.characters")
                ],
                [
                    KeyboardButton(text="buttons.counter_picks"),
                    KeyboardButton(text="buttons.builds")
                ],
                [
                    KeyboardButton(text="buttons.back")
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
                    KeyboardButton(text="buttons.build1"),
                    KeyboardButton(text="buttons.build2")
                ],
                [
                    KeyboardButton(text="buttons.back_to_navigation")
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
