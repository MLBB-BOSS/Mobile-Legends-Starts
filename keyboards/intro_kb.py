from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_intro_kb_1() -> InlineKeyboardMarkup:
    """Клавіатура для першої сторінки інтро"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Далі", callback_data="intro_next_1")]
        ]
    )

def get_intro_kb_2() -> InlineKeyboardMarkup:
    """Клавіатура для другої сторінки інтро"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Далі", callback_data="intro_next_2")]
        ]
    )

def get_intro_kb_3() -> InlineKeyboardMarkup:
    """Клавіатура для третьої сторінки інтро"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Розпочати", callback_data="intro_finish")]
        ]
    )
