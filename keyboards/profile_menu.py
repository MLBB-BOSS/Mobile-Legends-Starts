from aiogram.types import InlineKeyboardButton
from .base import BaseKeyboard

class ProfileMenuKeyboard(BaseKeyboard):
    @staticmethod
    def get_keyboard():
        buttons = [
            [InlineKeyboardButton(text="📈 Статистика", callback_data="profile_statistics")],
            [InlineKeyboardButton(text="🏅 Досягнення", callback_data="profile_achievements")],
            [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="profile_settings")],
            [InlineKeyboardButton(text="💌 Зворотний зв'язок", callback_data="profile_feedback")],
            [InlineKeyboardButton(text="❓ Допомога", callback_data="profile_help")],
            [InlineKeyboardButton(text="🔄 Назад", callback_data="back_to_main")],
        ]
        return BaseKeyboard.create_inline_keyboard(buttons)
