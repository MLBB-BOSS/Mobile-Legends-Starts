from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_tank_menu():
    """
    Створює меню для класу Tank.
    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Alice"), KeyboardButton(text="Tigreal"), KeyboardButton(text="Akai")],
            [KeyboardButton(text="Franco"), KeyboardButton(text="Minotaur"), KeyboardButton(text="Lolia")],
            [KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
