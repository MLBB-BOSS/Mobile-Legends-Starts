# keyboards/profile_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ProfileMenu:
    @staticmethod
    def get_profile_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📈 Статистика"), KeyboardButton("🏅 Досягнення")],
                [KeyboardButton("⚙️ Налаштування"), KeyboardButton("💌 Зворотний зв'язок")],
                [KeyboardButton("❓ Допомога"), KeyboardButton("🔄 Назад")]
            ],
            resize_keyboard=True
        )
