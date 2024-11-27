# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_guides_inline_menu():
    inline_keyboard = [
        [
            InlineKeyboardButton(text="🆕 Нові Гайди", callback_data="guide_new"),
            InlineKeyboardButton(text="🌟 Популярні Гайди", callback_data="guide_popular")
        ],
        [
            InlineKeyboardButton(text="📘 Для Початківців", callback_data="guide_beginner"),
            InlineKeyboardButton(text="🧙 Просунуті Техніки", callback_data="guide_advanced")
        ],
        [
            InlineKeyboardButton(text="🛡️ Командна Гра", callback_data="guide_teamplay")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_navigation")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
