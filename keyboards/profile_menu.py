# File: keyboards/profile_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ProfileMenu:
    @staticmethod
    def get_profile_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📈 Статистика"), KeyboardButton(text="🏅 Досягнення")],
                [KeyboardButton(text="⚙️ Налаштування"), KeyboardButton(text="💌 Зворотний зв'язок")],
                [KeyboardButton(text="🔄 Назад")]
            ],
            resize_keyboard=True
        )
