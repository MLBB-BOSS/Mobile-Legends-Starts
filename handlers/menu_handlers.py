# File: keyboards/profile_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the profile menu keyboard markup.
        Returns a simplified fallback keyboard if there's an error.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics") or "📊 Статистика"),
                        KeyboardButton(text=loc.get_message("buttons.achievements") or "🏆 Досягнення")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings") or "⚙️ Налаштування"),
                        KeyboardButton(text=loc.get_message("buttons.feedback") or "📝 Зворотній зв'язок")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення профільного меню: {e}")
            # Fallback keyboard with just the back button
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_statistics_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the statistics submenu keyboard markup.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.personal_stats") or "👤 Особиста статистика"),
                        KeyboardButton(text=loc.get_message("buttons.global_stats") or "🌐 Загальна статистика")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню статистики: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_achievements_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the achievements submenu keyboard markup.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.my_achievements") or "🏆 Мої досягнення"),
                        KeyboardButton(text=loc.get_message("buttons.leaderboard") or "🏅 Рейтинг")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню досягнень: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )
