from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.tanks")),
                        KeyboardButton(text=loc.get_message("buttons.fighters"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.assassins")),
                        KeyboardButton(text=loc.get_message("buttons.mages"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.marksmen")),
                        KeyboardButton(text=loc.get_message("buttons.supports"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню класів героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )
