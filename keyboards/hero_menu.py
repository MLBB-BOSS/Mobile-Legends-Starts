# File: keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.tanks")),
                        KeyboardButton(text=loc.get_message("buttons.fighters"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.assassins")),
                        KeyboardButton(text=loc.get_message("buttons.mages"))
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.marksmen")),
                        KeyboardButton(text=loc.get_message("buttons.supports"))
                    ],
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
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )

    def get_heroes_by_class(self, hero_class: str) -> ReplyKeyboardMarkup:
        try:
            heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")

            # Розбиваємо список героїв на групи по 2
            keyboard_buttons = []
            for i in range(0, len(heroes), 2):
                row = [KeyboardButton(text=hero) for hero in heroes[i:i+2]]
                keyboard_buttons.append(row)

            # Додаємо кнопку "Назад"
            keyboard_buttons.append([
                KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes"))
            ])

            return ReplyKeyboardMarkup(
                keyboard=keyboard_buttons,
                resize_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення списку героїв для класу {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.back"))]],
                resize_keyboard=True
            )
