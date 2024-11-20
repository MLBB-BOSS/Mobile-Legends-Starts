from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class ProfileMenu:
    """
    Клас для створення меню профілю
    """
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.my_stats")),
                        KeyboardButton(text=loc.get_message("buttons.my_heroes"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.my_achievements")),
                        KeyboardButton(text=loc.get_message("buttons.settings"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_main"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню профілю: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )
