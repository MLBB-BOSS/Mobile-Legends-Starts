# /keyboards/level2/navigation_menu.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

TEXTS = {
    "heroes": "🛡️ Персонажі",
    "guides": "📚 Гайди",
    "counter_picks": "⚖️ Контр-піки",
    "builds": "⚜️ Білди",
    "votes": "📊 Голосування",
    "back": "🔄 Назад"
}

def get_navigation_menu(row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Створює меню для навігації.

    :param row_width: Кількість кнопок у рядку (за замовчуванням 2).
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    buttons = [
        {"text": TEXTS["heroes"], "callback_data": "heroes_menu"},
        {"text": TEXTS["guides"], "callback_data": "guides_menu"},
        {"text": TEXTS["counter_picks"], "callback_data": "counter_picks_menu"},
        {"text": TEXTS["builds"], "callback_data": "builds_menu"},
        {"text": TEXTS["votes"], "callback_data": "votes_menu"},
        {"text": TEXTS["back"], "callback_data": "main_menu"}
    ]
    for button in buttons:
        builder.button(text=button["text"], callback_data=button["callback_data"])
    builder.adjust(row_width)
    return builder.as_markup()
