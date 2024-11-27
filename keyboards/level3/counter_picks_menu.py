from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_counter_picks_menu():
    """
    Створює клавіатуру для меню Контр-піків.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 Пошук Контр-піку"), KeyboardButton(text="📝 Список Персонажів"), KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
