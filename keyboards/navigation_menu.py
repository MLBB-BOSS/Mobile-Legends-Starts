from aiogram.types import InlineKeyboardButton
from .base import BaseKeyboard

class NavigationMenuKeyboard(BaseKeyboard):
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="🛡️ Персонажі", callback_data="menu_characters")],
            [InlineKeyboardButton(text="📚 Гайди", callback_data="menu_guides")],
            [InlineKeyboardButton(text="⚔️ Контр-піки", callback_data="menu_counterpicks")],
            [InlineKeyboardButton(text="⚜️ Білди", callback_data="menu_builds")],
            [InlineKeyboardButton(text="📊 Голосування", callback_data="menu_polls")],
            [InlineKeyboardButton(text="🔄 Назад", callback_data="back_to_main")],
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
