# keyboards/statistics_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StatisticsMenu:
    """Клавіатура для розділу 'Статистика' (3-й рівень)"""
    @staticmethod
    def get_statistics_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Загальна Активність"), KeyboardButton(text="🥇 Рейтинг")],
                [KeyboardButton(text="🎮 Ігрова Статистика"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
