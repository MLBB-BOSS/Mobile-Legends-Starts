# keyboards/main_menu.py - головне меню, кнопки "Навігація" і "Профіль"

from aiogram.types import InlineKeyboardButton
from keyboards.base import BaseKeyboard
from utils.localization import Localization

class MainMenuKeyboard(BaseKeyboard):
    @staticmethod
    def get_keyboard(lang="uk"):
        loc = Localization(lang)
        buttons = [
            [InlineKeyboardButton(text=loc.get_message("buttons.navigation"), callback_data="menu_navigation")],
            [InlineKeyboardButton(text=loc.get_message("buttons.profile"), callback_data="menu_profile")]
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
