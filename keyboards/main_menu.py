# keyboards/help_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class HelpMenu:
    """Клавіатура для розділу 'Допомога' (3-й рівень)"""
    @staticmethod
    def get_help_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📄 Інструкції"), KeyboardButton(text="❔ FAQ")],
                [KeyboardButton(text="📞 Підтримка")],
                [KeyboardButton(text="🔄 Назад до Профілю")],
            ],
            resize_keyboard=True
        )
