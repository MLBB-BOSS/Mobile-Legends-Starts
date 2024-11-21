# File: utils/localization.py

import json
import os
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class Localization:
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.messages: Dict[str, Any] = {}
        self._load_messages()

    def _load_messages(self) -> None:
        try:
            locale_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "locales",
                f"{self.lang}.json"
            )
            
            with open(locale_path, 'r', encoding='utf-8') as file:
                self.messages = json.load(file)
            logger.info(f"Successfully loaded messages for language: {self.lang}")
        except FileNotFoundError:
            logger.error(f"Failed to load messages: No such file: {locale_path}")
            self.messages = self._get_default_messages()
        except Exception as e:
            logger.error(f"Failed to load messages: {str(e)}")
            self.messages = self._get_default_messages()

    def get_message(self, key: str, **kwargs) -> str:
        try:
            current = self.messages
            for part in key.split('.'):
                current = current[part]

            if isinstance(current, str):
                # Handle both message_text and text parameters for backward compatibility
                if 'message_text' in kwargs and 'text' not in kwargs:
                    kwargs['text'] = kwargs.pop('message_text')
                return current.format(**kwargs)
            return str(current)
        except KeyError:
            logger.error(f"Missing localization key: {key}")
            return key
        except Exception as e:
            logger.error(f"Error getting message for key {key}: {str(e)}")
            return key

    def get_hero_info(self, hero_name: str) -> str:
        """Get hero information by name"""
        try:
            return self.messages["heroes"]["info"][hero_name]
        except KeyError:
            return f"Інформація про героя {hero_name} недоступна."

    def get_hero_class_name(self, class_key: str) -> str:
        """Get hero class name by key"""
        try:
            return self.messages["heroes"]["classes"][class_key]["name"]
        except KeyError:
            return class_key.capitalize()

    def get_heroes_by_class(self, class_key: str) -> list:
        """Get list of heroes by class"""
        try:
            return self.messages["heroes"]["classes"][class_key]["heroes"]
        except KeyError:
            return []

    def _get_default_messages(self) -> Dict[str, Any]:
        return {
            "buttons": {
                "navigation": "🧭 Навігація",
                "profile": "🪪 Мій Кабінет",
                "settings": "⚙️ Налаштування",
                "help": "❓ Допомога",
                "menu": "Меню",
                "show_heroes": "Показати героїв",
                "back_to_hero_classes": "⬅️ До класів героїв",
                "back_to_hero_list": "⬅️ До списку героїв",
                "statistics": "📊 Статистика",
                "achievements": "🏆 Досягнення",
                "feedback": "📝 Зворотній зв'язок",
                "back": "↩️ Назад",
                "guides": "📖 Гайди",
                "characters": "👥 Персонажі",
                "counter_picks": "⚔️ Контр-піки",
                "builds": "🛠️ Білди",
                "voting": "📊 Голосування",
                "back_to_navigation": "↩️ До навігації"
            },
            "messages": {
                "welcome": "Вітаємо у MLBB-BOSS! Це бот для організації та підтримки турнірів у грі Mobile Legends. Оберіть опцію з меню нижче.",
                "help": "Доступні команди:\n/start - Запустити бота\n/help - Отримати допомогу\n/profile - Мій профіль\n/settings - Налаштування\n\nДля додаткової інформації звертайтесь до адміністратора.",
                "unhandled_message": "Вибачте, я не розумію це повідомлення: {text}",
                "hero_menu": {
                    "select_hero": "Будь ласка, оберіть героя з класу {class_name}:"
                },
                "select_hero_class": "Оберіть клас героя:"
            },
            "errors": {
                "general": "Виникла непередбачена помилка. Будь ласка, спробуйте пізніше.",
                "class_not_found": "Вибраний клас героїв не знайдено. Будь ласка, оберіть з доступного списку.",
                "hero_not_found": "Вибраного героя не знайдено. Будь ласка, спробуйте інший вибір.",
                "not_registered": "Ви не зареєстровані. Використайте команду /start для реєстрації.",
                "permission_denied": "У вас немає доступу до цієї функції."
            }
        }

# Create a singleton instance
loc = Localization()

# Export both the class and the singleton instance
__all__ = ['Localization', 'loc']
