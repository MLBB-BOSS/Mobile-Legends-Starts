# keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """
    Повертає головну клавіатуру.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Мій Профіль")],
            [KeyboardButton(text="❓ Допомога"), KeyboardButton(text="💌 Зворотний Зв'язок")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Оберіть категорію:"
    )
