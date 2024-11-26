# /keyboards/level2/navigation_menu.py
# Навігація - другий рівень

from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_navigation_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛡️ Персонажі", callback_data="heroes_menu")
    builder.button(text="📚 Гайди", callback_data="guides_menu")
    builder.button(text="⚖️ Контр-піки", callback_data="counter_picks_menu")
    builder.button(text="⚜️ Білди", callback_data="builds_menu")
    builder.button(text="📊 Голосування", callback_data="votes_menu")
    builder.button(text="🔄 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()

