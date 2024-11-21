from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization_instance import loc
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.navigation")),
                    KeyboardButton(text=loc.get_message("buttons.profile"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.settings")),
                    KeyboardButton(text=loc.get_message("buttons.feedback"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
