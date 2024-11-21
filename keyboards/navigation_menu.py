# File: keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        """Creates and returns the main navigation menu keyboard"""
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.guides") or "📖 Гайди"),
                        KeyboardButton(text=loc.get_message("buttons.characters") or "👥 Персонажі")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.counter_picks") or "⚔️ Контр-піки"),
                        KeyboardButton(text=loc.get_message("buttons.builds") or "🛠️ Білди")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.voting") or "📊 Голосування")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення навігаційного меню: {e}")
            # Return a simplified fallback keyboard
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        """Creates and returns the heroes menu keyboard"""
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.tank.name") or "Танк"),
                        KeyboardButton(text=loc.get_message("heroes.classes.fighter.name") or "Бійці")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.assassin.name") or "Асасини"),
                        KeyboardButton(text=loc.get_message("heroes.classes.mage.name") or "Маги")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.marksman.name") or "Стрільці"),
                        KeyboardButton(text=loc.get_message("heroes.classes.support.name") or "Підтримка")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_navigation") or "↩️ До навігації")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ До навігації")]
                ],
                resize_keyboard=True
            )

    def get_hero_class_menu(self, hero_class: str) -> ReplyKeyboardMarkup:
        """Creates and returns the menu for a specific hero class"""
        try:
            heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")
            if not heroes:
                raise ValueError(f"Heroes not found for class: {hero_class}")

            # Split heroes into pairs for the keyboard
            hero_pairs = [heroes[i:i + 2] for i in range(0, len(heroes), 2)]
            keyboard_buttons = [[KeyboardButton(text=hero) for hero in pair] for pair in hero_pairs]
            
            # Add back button
            keyboard_buttons.append([
                KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes") or "⬅️ До класів героїв")
            ])

            return ReplyKeyboardMarkup(
                keyboard=keyboard_buttons,
                resize_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню класу героїв {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="⬅️ До класів героїв")]
                ],
                resize_keyboard=True
            )
