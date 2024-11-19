from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.localization.localize import get_message as _

class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=_("buttons.statistics")),
                    KeyboardButton(text=_("buttons.achievements"))
                ],
                [
                    KeyboardButton(text=_("buttons.settings")),
                    KeyboardButton(text=_("buttons.feedback"))
                ],
                [KeyboardButton(text=_("buttons.back"))]
            ],
            resize_keyboard=True
        )
        return keyboard
