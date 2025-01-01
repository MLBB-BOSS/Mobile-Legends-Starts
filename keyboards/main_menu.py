from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавіатура головного меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація")],
            [KeyboardButton(text="🪪 Мій Профіль")]
        ],
        resize_keyboard=True
    )

def get_main_menu_inline() -> InlineKeyboardMarkup:
    """Інлайн клавіатура для головного меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧭 Навігація", callback_data="navigation")],
            [InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="profile")]
        ]
    )

# Other functions...
