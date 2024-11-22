# keyboards/characters_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class CharactersMenu:
    @staticmethod
    def get_characters_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
                [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін")],
                [KeyboardButton(text="🤝 Підтримка"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
