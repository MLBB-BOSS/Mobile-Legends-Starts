from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        try:
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
        except Exception as e:
            logger.error(f"Помилка створення меню навігації: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="❌ Помилка")]],
                resize_keyboard=True
            )
