from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .base import BaseKeyboard

class MainMenu(BaseKeyboard):
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="🛡️ Герої", callback_data="menu_heroes")],
            [InlineKeyboardButton(text="⚜️ Білди", callback_data="menu_builds")],
            [InlineKeyboardButton(text="📊 Турніри", callback_data="menu_tournaments")],
            [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="menu_settings")],
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
