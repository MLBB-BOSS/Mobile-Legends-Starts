# /keyboards/level1/main_menu.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

TEXTS = {
    "navigation": "🧭 Навігація",
    "profile": "🪪 Профіль"
}

def get_main_menu(row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Створює головну клавіатуру бота.

    :param row_width: Кількість кнопок у рядку (за замовчуванням 2).
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    buttons = [
        {"text": TEXTS["navigation"], "callback_data": "navigation_menu"},
        {"text": TEXTS["profile"], "callback_data": "profile_menu"}
    ]
    for button in buttons:
        builder.button(text=button["text"], callback_data=button["callback_data"])
    builder.adjust(row_width)
    return builder.as_markup()
