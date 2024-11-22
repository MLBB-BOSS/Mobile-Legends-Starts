# keyboards/achievements_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_achievements_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎖️ Мої Бейджі"), KeyboardButton(text="🚀 Прогрес")],
            [KeyboardButton(text="🏅 Турнірна Статистика"), KeyboardButton(text="🔄 Назад до Профілю")],
        ],
        resize_keyboard=True
    )
