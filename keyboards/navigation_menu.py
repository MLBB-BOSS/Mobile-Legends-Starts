# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_menu():
    """
    Повертає клавіатуру для навігації з кнопками.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Персонажі"), KeyboardButton(text="Гайди")],
            [KeyboardButton(text="Контр-піки"), KeyboardButton(text="Білди")],
            [KeyboardButton(text="Назад")]  # Кнопка для повернення
        ],
        resize_keyboard=True,  # Робить кнопки компактними
        one_time_keyboard=False  # Залишає клавіатуру після вибору
    )
