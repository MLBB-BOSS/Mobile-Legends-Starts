# keyboards/inline_keyboards.py

# -------------------------
# 📦 Імпорти
# -------------------------
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# -------------------------
# 📝 Функції Створення Інлайн-Клавіатур
# -------------------------

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Базова клавіатура з загальними кнопками.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="MLS Button",
                    callback_data="mls_button"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад до меню",
                    callback_data="menu_back"
                )
            ],
        ]
    )
    return keyboard

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для першої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Далі",
                    callback_data="intro_next_1"
                )
            ],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для другої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Далі",
                    callback_data="intro_next_2"
                )
            ],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для третьої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Розпочати",
                    callback_data="intro_start"
                )
            ],
        ]
    )
    return keyboard

def get_back_to_main_menu_button() -> InlineKeyboardMarkup:
    """
    Клавіатура з єдиною декоративною кнопкою для повернення до головного меню.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="═══════════════════╗\n║        ░▒▓█ Ｍ Ｌ Ｓ █▓▒░",
                    callback_data="menu_back"
                )
            ]
        ]
    )
    return keyboard

def get_main_menu() -> InlineKeyboardMarkup:
    """
    Генерує клавіатуру для головного меню з кнопками "Новини" та "Виклики".
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📰 Новини",
                    callback_data="news_placeholder"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎯 Виклики",
                    callback_data="challenges_placeholder"
                )
            ],
        ]
    )
    return keyboard