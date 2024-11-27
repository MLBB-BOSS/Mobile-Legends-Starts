from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_guides_menu():
    """
    Створює клавіатуру для меню гайдів.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆕 Нові Гайди"), KeyboardButton(text="🌟 Популярні Гайди"), KeyboardButton(text="📘 Для Початківців")],
            [KeyboardButton(text="🧙 Просунуті Техніки"), KeyboardButton(text="🛡️ Командна Гра"), KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
