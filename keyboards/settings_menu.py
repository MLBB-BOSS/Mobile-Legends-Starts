# keyboards/settings_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class SettingsMenu:
    """Клавіатура для розділу 'Налаштування' (3-й рівень)"""
    @staticmethod
    def get_settings_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌐 Мова Інтерфейсу"), KeyboardButton(text="🆔 Змінити Username")],
                [KeyboardButton(text="🛡️ Оновити ID Гравця"), KeyboardButton(text="🔔 Сповіщення")],
                [KeyboardButton(text="🔄 Назад до Профілю")],
            ],
            resize_keyboard=True
        )
