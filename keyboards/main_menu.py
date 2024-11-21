# File: keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.localization import loc

class MainMenu:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """Create and return the main menu keyboard"""
        try:
            self.builder.row(
                KeyboardButton(text=loc.get_message("buttons.navigation")),
                KeyboardButton(text=loc.get_message("buttons.characters"))
            )
            
            return self.builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        except Exception as e:
            logger.error(f"Error creating main menu: {str(e)}")
            # Return a basic fallback keyboard if localization fails
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="📱 Навігація"),
                        KeyboardButton(text="👥 Герої")
                    ]
                ],
                resize_keyboard=True
            )
