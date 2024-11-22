# keyboards/voting_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class VotingMenu:
    """Клавіатура для розділу 'Голосування' (3-й рівень)"""
    @staticmethod
    def get_voting_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Поточні Опитування"), KeyboardButton(text="📋 Мої Голосування")],
                [KeyboardButton(text="➕ Запропонувати Тему"), KeyboardButton(text="🔄 Назад до Навігації")],
            ],
            resize_keyboard=True
        )
