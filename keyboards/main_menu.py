# Шлях: keyboards/main_menu.py
# Цей файл містить класи для створення головного меню та базову структуру для всіх меню
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional, List
from .utils import create_keyboard_row

class BaseMenu:
    """Базовий клас для всіх меню"""
    async def get_keyboard(self, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
        """Базовий метод для отримання клавіатури"""
        raise NotImplementedError
    
    async def get_text(self, user_id: Optional[int] = None) -> str:
        """Базовий метод для отримання тексту меню"""
        raise NotImplementedError

class MainMenu(BaseMenu):
    """Клас для створення головного меню"""
    def __init__(self):
        # Визначаємо всі кнопки меню
        self.buttons = {
            'heroes': {'text': "🦸‍♂️ Герої", 'callback_data': "menu_heroes"},
            'builds': {'text': "🛠️ Білди", 'callback_data': "menu_builds"},
            'guides': {'text': "📖 Гайди", 'callback_data': "menu_guides"},
            'stats': {'text': "📊 Статистика", 'callback_data': "menu_statistics"},
            'profile': {'text': "👤 Профіль", 'callback_data': "menu_profile"},
            'settings': {'text': "⚙️ Налаштування", 'callback_data': "menu_settings"},
        }

    async def get_keyboard(self, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
        """Створює та повертає клавіатуру головного меню"""
        keyboard = [
            # Створюємо ряди кнопок по 2 в кожному
            create_keyboard_row(self.buttons['heroes'], self.buttons['builds']),
            create_keyboard_row(self.buttons['guides'], self.buttons['stats']),
            create_keyboard_row(self.buttons['profile'], self.buttons['settings'])
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_text(self, user_id: Optional[int] = None) -> str:
        """Повертає текст, який буде показано над клавіатурою"""
        return (
            "🎮 Ласкаво просимо до Mobile Legends Assistant!\n\n"
            "Оберіть розділ для навігації:"
        )
