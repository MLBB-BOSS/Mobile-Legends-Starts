from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    """
    Створює клавіатуру головного меню.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡️ Персонажі", callback_data="menu_heroes"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="menu_stats")
        ],
        [
            InlineKeyboardButton(text="🏆 Турніри", callback_data="menu_tournaments"),
            InlineKeyboardButton(text="⚙️ Налаштування", callback_data="menu_settings")
        ]
    ])
    return keyboard
