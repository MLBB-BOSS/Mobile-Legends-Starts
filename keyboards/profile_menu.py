from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc  # Змінений імпорт

class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
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
                [KeyboardButton(text=loc.get_message("buttons.back"))]
            ],
            resize_keyboard=True
        )
        return keyboard
