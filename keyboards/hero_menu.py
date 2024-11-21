# keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    """
    Клас для створення меню класів героїв
    """
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        try:
            classes = loc.get_hero_classes()
            buttons = [
                [KeyboardButton(text=cls.capitalize())] for cls in classes
            ]
            keyboard = ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            logger.info("Меню класів героїв успішно створено.")
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню класів героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )

    def get_heroes_by_class(self, hero_class: str) -> ReplyKeyboardMarkup:
        try:
            heroes = loc.messages['heroes']['classes'][hero_class.lower()]['heroes']
            buttons = [
                [KeyboardButton(text=hero)] for hero in heroes
            ]
            keyboard = ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            logger.info(f"Меню героїв для класу {hero_class} успішно створено.")
            return keyboard
        except KeyError:
            logger.error(f"Клас героїв {hero_class} не знайдено.")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню героїв для класу {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )
