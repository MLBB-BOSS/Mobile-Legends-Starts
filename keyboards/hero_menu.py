# keyboards/heroes_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class HeroesMenu:
    """Клавіатура для розділу 'Герої' (3-й рівень)"""
    @staticmethod
    def get_heroes_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔎 Пошук Героя")],
                [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
                [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін")],
                [KeyboardButton(text="🧬 Підтримка"), KeyboardButton(text="🔄 Назад до Навігації")],
            ],
            resize_keyboard=True
        )
