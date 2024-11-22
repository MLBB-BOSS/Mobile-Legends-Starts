# keyboards/menus.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    """Клавіатура головного меню"""
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Мій профіль")],
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
                [KeyboardButton(text="ℹ️ Допомога")],  # Додано кнопку «Допомога»
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class CharactersMenu:
    """Клавіатура для розділу 'Персонажі' (3-й рівень)"""
    @staticmethod
    def get_characters_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
                [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін")],
                [KeyboardButton(text="🤝 Підтримка"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class StatisticsMenu:
    """Клавіатура для розділу 'Статистика' (3-й рівень)"""
    @staticmethod
    def get_statistics_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Загальна Активність"), KeyboardButton(text="🥇 Рейтинг")],
                [KeyboardButton(text="🎮 Ігрова Статистика"), KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )

class HelpMenu:
    """Клавіатура для розділу 'Допомога' (3-й рівень)"""
    @staticmethod
    def get_help_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Як користуватися ботом"), KeyboardButton(text="Контакти")],
                [KeyboardButton(text="🔄 Назад")],
            ],
            resize_keyboard=True
        )
