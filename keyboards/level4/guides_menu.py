# /keyboards/level4/guides_menu.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

TEXTS = {
    "new_guides": "🆕 Нові Гайди",
    "popular_guides": "🌟 Популярні Гайди",
    "beginner_guides": "📘 Для Початківців",
    "advanced_guides": "🧙 Просунуті Техніки",
    "teamplay_guides": "🛡️ Командна Гра",
    "back": "🔄 Назад"
}

def get_guides_menu(row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Створює меню для гайдів.

    :param row_width: Кількість кнопок у рядку (за замовчуванням 2).
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    buttons = [
        {"text": TEXTS["new_guides"], "callback_data": "new_guides"},
        {"text": TEXTS["popular_guides"], "callback_data": "popular_guides"},
        {"text": TEXTS["beginner_guides"], "callback_data": "beginner_guides"},
        {"text": TEXTS["advanced_guides"], "callback_data": "advanced_guides"},
        {"text": TEXTS["teamplay_guides"], "callback_data": "teamplay_guides"},
        {"text": TEXTS["back"], "callback_data": "navigation_menu"}
    ]
    for button in buttons:
        builder.button(text=button["text"], callback_data=button["callback_data"])
    builder.adjust(row_width)
    return builder.as_markup()
