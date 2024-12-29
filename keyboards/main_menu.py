from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавіатура головного меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація")],
            [KeyboardButton(text="🪪 Мій Профіль")]
        ],
        resize_keyboard=True
    )

def get_main_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Інлайн клавіатура для екрану головного меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📱 Наш канал", url="https://t.me/mlbb_boss"),
                InlineKeyboardButton(text="💬 Чат", url="https://t.me/mlbb_boss_chat")
            ]
        ]
    )
