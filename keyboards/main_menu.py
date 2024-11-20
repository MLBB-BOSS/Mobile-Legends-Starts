# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class MainMenu:
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """
        Створює головне меню з кнопками навігації та профілю
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    # Перший ряд: Навігація та Профіль
                    [
                        KeyboardButton(text=loc.get_message("buttons.navigation")),
                        KeyboardButton(text=loc.get_message("buttons.profile"))
                    ],
                    # Другий ряд: Персонажі та Гайди
                    [
                        KeyboardButton(text=loc.get_message("buttons.characters")),
                        KeyboardButton(text=loc.get_message("buttons.guides"))
                    ],
                    # Третій ряд: Статистика та Досягнення
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics")),
                        KeyboardButton(text=loc.get_message("buttons.achievements"))
                    ],
                    # Четвертий ряд: Налаштування
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
            
        except Exception as e:
            logger.error(f"Помилка створення головного меню: {e}")
            # Повертаємо спрощене меню у випадку помилки
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=loc.get_message("buttons.menu"))]
                ],
                resize_keyboard=True
            )
    
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        """
        Створює меню навігації
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    # Перший ряд: Герої та Контр-піки
                    [
                        KeyboardButton(text=loc.get_message("buttons.characters")),
                        KeyboardButton(text=loc.get_message("buttons.counter_picks"))
                    ],
                    # Другий ряд: Збірки та Гайди
                    [
                        KeyboardButton(text=loc.get_message("buttons.builds")),
                        KeyboardButton(text=loc.get_message("buttons.guides"))
                    ],
                    # Третій ряд: Статистика та Голосування
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics")),
                        KeyboardButton(text=loc.get_message("buttons.voting"))
                    ],
                    # Четвертий ряд: Назад до головного меню
                    [
                        KeyboardButton(text=loc.get_message("buttons.main_menu"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
            
        except Exception as e:
            logger.error(f"Помилка створення меню навігації: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=loc.get_message("buttons.back"))]
                ],
                resize_keyboard=True
            )

    def get_heroes_class_menu(self) -> ReplyKeyboardMarkup:
        """
        Створює меню вибору класу героїв
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    # Перший ряд: Танки та Бійці
                    [
                        KeyboardButton(text=loc.get_message("buttons.tanks")),
                        KeyboardButton(text=loc.get_message("buttons.fighters"))
                    ],
                    # Другий ряд: Асасини та Маги
                    [
                        KeyboardButton(text=loc.get_message("buttons.assassins")),
                        KeyboardButton(text=loc.get_message("buttons.mages"))
                    ],
                    # Третій ряд: Стрільці та Підтримка
                    [
                        KeyboardButton(text=loc.get_message("buttons.marksmen")),
                        KeyboardButton(text=loc.get_message("buttons.supports"))
                    ],
                    # Четвертий ряд: Назад
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
            
        except Exception as e:
            logger.error(f"Помилка створення меню класів героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=loc.get_message("buttons.back"))]
                ],
                resize_keyboard=True
                        )
