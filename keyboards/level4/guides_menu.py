# /keyboards/level4/guides_menu.py
# 📚 Гайди - четвертий рівень

from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_guides_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Нові Гайди", callback_data="new_guides")
    builder.button(text="🌟 Популярні Гайди", callback_data="popular_guides")
    builder.button(text="📘 Для Початківців", callback_data="beginner_guides")
    builder.button(text="🧙 Просунуті Техніки", callback_data="advanced_guides")
    builder.button(text="🛡️ Командна Гра", callback_data="teamplay_guides")
    builder.button(text="🔄 Назад", callback_data="navigation_menu")
    builder.adjust(2)
    return builder.as_markup()
