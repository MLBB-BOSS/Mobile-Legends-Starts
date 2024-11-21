from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics")),
                        KeyboardButton(text=loc.get_message("buttons.achievements"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings")),
                        KeyboardButton(text=loc.get_message("buttons.feedback"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення профільного меню: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )
