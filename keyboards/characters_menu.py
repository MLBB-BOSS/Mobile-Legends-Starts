# keyboards/characters_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class CharactersMenu:
    """Клавіатура для розділу 'Персонажі' (3-й рівень)"""
    @staticmethod
    def get_characters_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
                [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін")],
                [KeyboardButton(text="🤝 Підтримка"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
