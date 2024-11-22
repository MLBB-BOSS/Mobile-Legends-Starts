from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    """Клавіатура головного меню"""
    @staticmethod
    def get_main_menu():
        logger.info("Створення клавіатури головного меню")
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Мій профіль")],
                [KeyboardButton(text="ℹ️ Допомога")],
            ],
            resize_keyboard=True
        )

class NavigationMenu:
    """Клавіатура для навігації (2-й рівень)"""
    @staticmethod
    def get_navigation_menu():
        logger.info("Створення клавіатури для навігації (2-й рівень)")
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Місця"), KeyboardButton(text="Події")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class ProfileMenu:
    """Клавіатура для профілю (2-й рівень)"""
    @staticmethod
    def get_profile_menu():
        logger.info("Створення клавіатури для профілю (2-й рівень)")
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Налаштування")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class SubMenu:
    """Клавіатура підменю (3-й рівень)"""
    @staticmethod
    def get_sub_menu():
        logger.info("Створення клавіатури підменю (3-й рівень)")
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Дія 1"), KeyboardButton(text="Дія 2")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
