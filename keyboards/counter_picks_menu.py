# keyboards/counter_picks_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class CounterPicksMenu:
    """Клавіатура для розділу 'Контр-піки' (3-й рівень)"""
    @staticmethod
    def get_counter_picks_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔎 Пошук Контр-піку"), KeyboardButton(text="📝 Список Героїв")],
                [KeyboardButton(text="🔄 Назад до Навігації")],
            ],
            resize_keyboard=True
        )
