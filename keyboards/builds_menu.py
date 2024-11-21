from aiogram.types import InlineKeyboardButton
from .base import BaseKeyboard

class BuildsMenuKeyboard(BaseKeyboard):
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="⚙️ Створити Білд", callback_data="create_build")],
            [InlineKeyboardButton(text="📜 Мої Білди", callback_data="my_builds")],
            [InlineKeyboardButton(text="🔥 Популярні Білди", callback_data="popular_builds")],
            [InlineKeyboardButton(text="🔄 Назад", callback_data="back_to_navigation")],
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
