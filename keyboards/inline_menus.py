from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    """Функція для створення клавіатури головного меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Профіль", callback_data="menu_profile")],
        [InlineKeyboardButton(text="Статистика", callback_data="menu_stats")],
        [InlineKeyboardButton(text="Команда", callback_data="menu_team")],
        [InlineKeyboardButton(text="Турніри", callback_data="menu_tournament")],
    ])
    return keyboard

def get_intro_page_1_keyboard():
    """Функція для створення клавіатури для першої сторінки вступу"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Продовжити", callback_data="intro_page_2")],
    ])
    return keyboard

def get_intro_page_2_keyboard():
    """Функція для створення клавіатури для другої сторінки вступу"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Продовжити", callback_data="intro_page_3")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="intro_page_1")],
    ])
    return keyboard

def get_intro_page_3_keyboard():
    """Функція для створення клавіатури для третьої сторінки вступу"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Розпочати", callback_data="intro_finish")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="intro_page_2")],
    ])
    return keyboard
