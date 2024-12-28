# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Базова клавіатура з загальними кнопками.
    """
    logger.info("Створення базової inline клавіатури")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="MLS Button", callback_data="mls_button")],
            [InlineKeyboardButton(text="Назад до меню", callback_data="menu_back")],
        ]
    )
    return keyboard


def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для першої сторінки інтро.
    """
    logger.info("Створення inline клавіатури для першої інтро сторінки")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard


def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для другої сторінки інтро.
    """
    logger.info("Створення inline клавіатури для другої інтро сторінки")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard


def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для третьої сторінки інтро.
    """
    logger.info("Створення inline клавіатури для третьої інтро сторінки")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard


def get_back_to_main_menu_button() -> InlineKeyboardMarkup:
    """
    Клавіатура з єдиною кнопкою для повернення до головного меню.
    """
    logger.info("Створення кнопки повернення до головного меню")
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


def get_inline_main_menu() -> InlineKeyboardMarkup:
    """
    Генерує inline клавіатуру для головного меню з кнопками "Новини" та "Виклики".
    """
    logger.info("Створення inline клавіатури головного меню")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📰 Новини", callback_data="news_placeholder")],
            [InlineKeyboardButton(text="🎯 Виклики", callback_data="challenges_placeholder")],
        ]
    )
    return keyboard


# Додаємо експорт всіх функцій
__all__ = [
    'get_generic_inline_keyboard',
    'get_intro_page_1_keyboard',
    'get_intro_page_2_keyboard',
    'get_intro_page_3_keyboard',
    'get_back_to_main_menu_button',
    'get_inline_main_menu'
]
