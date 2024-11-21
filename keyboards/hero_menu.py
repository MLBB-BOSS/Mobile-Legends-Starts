from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    """
    Клас для створення меню класів героїв та списку героїв
    """
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        try:
            classes = loc.get_message("heroes.classes")
            buttons = [
                KeyboardButton(text=class_info["name"]) for class_info in classes.values()
            ]
            # Розподіляємо кнопки по рядках
            keyboard = []
            for i in range(0, len(buttons), 2):
                keyboard.append(buttons[i:i+2])

            return ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню класів героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )

    def get_heroes_by_class(self, hero_class: str) -> ReplyKeyboardMarkup:
        try:
            heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")
            buttons = [KeyboardButton(text=hero) for hero in heroes]
            # Розподіляємо кнопки по рядках
            keyboard = []
            for i in range(0, len(buttons), 2):
                keyboard.append(buttons[i:i+2])

            # Додаємо кнопку "Назад"
            keyboard.append([KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes"))])

            return ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню героїв для класу {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )
