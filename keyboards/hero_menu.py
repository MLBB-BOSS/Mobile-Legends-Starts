# keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_hero_class_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг"), KeyboardButton(text="🏹 Стрілець")],
            [KeyboardButton(text="⚔️ Асасін"), KeyboardButton(text="🧬 Підтримка"), KeyboardButton(text="🤺 Боєць")],
            [KeyboardButton(text="🔄 Назад")]
        ],
        resize_keyboard=True
    )
