# File: keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        """Creates and returns the main menu keyboard"""
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.navigation")),
                        KeyboardButton(text=loc.get_message("buttons.profile"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings")),
                        KeyboardButton(text=loc.get_message("buttons.help"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Error creating main menu: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❓ Меню")]],
                resize_keyboard=True
            )
