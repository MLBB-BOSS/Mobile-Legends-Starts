from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class NavigationMenu:
    """
    Клас для створення меню навігації
    """
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.characters")),
                        KeyboardButton(text=loc.get_message("buttons.guides"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics")),
                        KeyboardButton(text=loc.get_message("buttons.achievements"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_main"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню навігації: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )
