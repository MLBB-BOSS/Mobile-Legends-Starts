# keyboards/game_modes_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class GameModesMenu:
    """Клавіатура для розділу 'Режими Гри' (3-й рівень)"""
    @staticmethod
    def get_game_modes_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🪩 Класичний"), KeyboardButton(text="🎮 Рейтинг")],
                [KeyboardButton(text="🎭 Події"), KeyboardButton(text="🔄 Назад до Навігації")],
            ],
            resize_keyboard=True
        )
