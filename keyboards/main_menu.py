from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        # Local import to avoid circular import
        from utils.localization_instance import loc
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
