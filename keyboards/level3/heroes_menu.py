# /keyboards/level3/heroes_menu.py
#  Персонажі - третій рівень

from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_heroes_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔎 Пошук Персонажа", callback_data="search_hero")
    builder.button(text="🛡️ Танк", callback_data="tank_heroes")
    builder.button(text="🔮 Маг", callback_data="mage_heroes")
    builder.button(text="🏹 Стрілець", callback_data="marksman_heroes")
    builder.button(text="⚔️ Асасін", callback_data="assassin_heroes")
    builder.button(text="🧬 Підтримка", callback_data="support_heroes")
    builder.button(text="🔄 Назад", callback_data="navigation_menu")
    builder.adjust(2)
    return builder.as_markup()

