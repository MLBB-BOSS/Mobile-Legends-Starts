from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        buttons = [
            [
                KeyboardButton(text=loc.get_message("buttons.navigation")),  # "🧭 Навігація"
                KeyboardButton(text=loc.get_message("buttons.profile"))      # "🪪 Мій Кабінет"
            ]
        ]
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
