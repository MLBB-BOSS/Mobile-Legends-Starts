# keyboards/main_menu.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Клавіатури для головного меню та підменю

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationKeyboards:
    @staticmethod
    def main_navigation() -> ReplyKeyboardMarkup:
        """Головне меню навігації"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
            [KeyboardButton(text="🛡️ Персонажі")],
            [KeyboardButton(text="📖 Гайди")],
            [KeyboardButton(text="⚔️ Контр-піки"), KeyboardButton(text="🛠️ Білди")],
            [KeyboardButton(text="🔙 Назад до головного меню")]
        ])
        return keyboard

    @staticmethod
    def heroes_submenu() -> ReplyKeyboardMarkup:
        """Меню для вибору класу героїв"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
            [KeyboardButton(text="🔍 Пошук персонажа")],
            [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
            [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="🗡️ Асасін")],
            [KeyboardButton(text="🤝 Підтримка")],
            [KeyboardButton(text="🔙 Назад до навігації")]
        ])
        return keyboard

class ProfileKeyboards:
    @staticmethod
    def main_profile() -> ReplyKeyboardMarkup:
        """Головне меню профілю"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
            [KeyboardButton(text="📈 Статистика"), KeyboardButton(text="🏅 Досягнення")],
            [KeyboardButton(text="⚙️ Налаштування"), KeyboardButton(text="💌 Зворотний зв'язок")],
            [KeyboardButton(text="🔙 Назад до головного меню")]
        ])
        return keyboard

    @staticmethod
    def stats_submenu() -> ReplyKeyboardMarkup:
        """Меню статистики"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
            [KeyboardButton(text="📊 Загальна активність")],
            [KeyboardButton(text="🥇 Рейтинг"), KeyboardButton(text="🎮 Ігрова статистика")],
            [KeyboardButton(text="🔙 Назад до профілю")]
        ])
        return keyboard

    @staticmethod
    def settings_submenu() -> ReplyKeyboardMarkup:
        """Меню налаштувань профілю"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
            [KeyboardButton(text="🌐 Мова інтерфейсу")],
            [KeyboardButton(text="🆔 Змінити Username"), KeyboardButton(text="🎯 Оновити ID гравця")],
            [KeyboardButton(text="🔔 Налаштування сповіщень")],
            [KeyboardButton(text="🔙 Назад до профілю")]
        ])
        return keyboard
