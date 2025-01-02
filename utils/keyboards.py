# utils/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧭 Навігація"),
                KeyboardButton(text="🪪 Мій Профіль")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Виберіть опцію..."
    )

def get_navigation_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎮 Герої"),
                KeyboardButton(text="🗺 Карта")
            ],
            [
                KeyboardButton(text="⚔️ Предмети"),
                KeyboardButton(text="🏆 Ранги")
            ],
            [
                KeyboardButton(text="📖 Гайди"),
                KeyboardButton(text="🔄 Мета")
            ],
            [
                KeyboardButton(text="🔙 Головне меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Оберіть розділ..."
    )

def get_generic_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ℹ️ Деталі", callback_data="details"),
                InlineKeyboardButton(text="📋 Список", callback_data="list")
            ]
        ]
    )
