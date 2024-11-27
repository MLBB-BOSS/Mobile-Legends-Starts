from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_guides_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆕 Нові Гайди"), KeyboardButton(text="🌟 Популярні Гайди")],
            [KeyboardButton(text="📘 Для Початківців"), KeyboardButton(text="🧙 Просунуті Техніки")],
            [KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
