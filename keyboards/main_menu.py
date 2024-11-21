# keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    """
    Клас для створення головного меню бота
    """
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                [
                    KeyboardButton(text=loc.get_message("buttons.navigation")),
                    KeyboardButton(text=loc.get_message("buttons.profile"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.settings")),
                    KeyboardButton(text=loc.get_message("buttons.help"))
                ]
            ]
            keyboard.keyboard = buttons
            logger.info("Головне меню успішно створено.")
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення головного меню: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )
