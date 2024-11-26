# /keyboards/level3/heroes_menu.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

TEXTS = {
    "search": "🔎 Пошук Персонажа",
    "tank": "🛡️ Танк",
    "mage": "🔮 Маг",
    "marksman": "🏹 Стрілець",
    "assassin": "⚔️ Асасін",
    "support": "🧬 Підтримка",
    "back": "🔄 Назад"
}

def get_heroes_menu(row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Створює меню для персонажів.

    :param row_width: Кількість кнопок у рядку (за замовчуванням 2).
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    buttons = [
        {"text": TEXTS["search"], "callback_data": "search_hero"},
        {"text": TEXTS["tank"], "callback_data": "tank_heroes"},
        {"text": TEXTS["mage"], "callback_data": "mage_heroes"},
        {"text": TEXTS["marksman"], "callback_data": "marksman_heroes"},
        {"text": TEXTS["assassin"], "callback_data": "assassin_heroes"},
        {"text": TEXTS["support"], "callback_data": "support_heroes"},
        {"text": TEXTS["back"], "callback_data": "navigation_menu"}
    ]
    for button in buttons:
        builder.button(text=button["text"], callback_data=button["callback_data"])
    builder.adjust(row_width)
    return builder.as_markup()
