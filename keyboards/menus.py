# keyboards/menus.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    """Клавіатура головного меню"""
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
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
    def get_navigation_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Місця"), KeyboardButton(text="Події")],
                [KeyboardButton(text="Персонажі"), KeyboardButton(text="Гайди")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class ProfileMenu:
    """Клавіатура для профілю (2-й рівень)"""
    @staticmethod
    def get_profile_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Налаштування")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
