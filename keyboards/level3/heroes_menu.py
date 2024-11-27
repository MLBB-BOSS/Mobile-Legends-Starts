from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_heroes_menu():
    """
    Створює клавіатуру третього рівня з трьома колонками.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 Пошук Персонажа"), KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
            [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін"), KeyboardButton(text="🧬 Підтримка")],
            [KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
