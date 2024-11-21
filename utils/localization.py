# File: utils/localization.py

import json
import os
import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class Localization:
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.messages: Dict[str, Any] = {}
        self._load_messages()

    def _load_messages(self) -> None:
        """Load messages from JSON file"""
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
        """
        Get localized message by key with parameter substitution
        
        Args:
            key: The dot-notation key for the message
            **kwargs: Parameters to substitute in the message
        """
        try:
            # Split the key by dots and traverse the messages dict
            current = self.messages
            for part in key.split('.'):
                current = current[part]

            # If we got a string, format it with parameters
            if isinstance(current, str):
                return current.format(**kwargs)
            
            return str(current)
        except KeyError:
            logger.error(f"Missing localization key: {key}")
            return key
        except Exception as e:
            logger.error(f"Error getting message for key {key}: {str(e)}")
            return key

    def _get_default_messages(self) -> Dict[str, Any]:
        """Return default messages when locale file is not found"""
        return {
            "messages": {
                "unhandled_message": "Вибачте, я не розумію команду: {text}",
                "welcome": "Ласкаво просимо до MLS Bot!",
                "error": "Виникла помилка. Спробуйте ще раз.",
                "navigation_menu": "Оберіть розділ для навігації:",
                "hero_menu": {
                    "select_hero": "Оберіть героя класу {class_name}:"
                }
            },
            "buttons": {
                "navigation": "📱 Навігація",
                "characters": "👥 Герої",
                "back": "↩️ Назад",
                "back_to_navigation": "↩️ До навігації",
                "back_to_hero_classes": "↩️ До класів героїв",
                "back_to_hero_list": "↩️ До списку героїв",
                "show_heroes": "👥 Показати героїв",
                "tanks": "🛡️ Танки",
                "fighters": "⚔️ Файтери",
                "assassins": "🗡️ Асасини",
                "mages": "🔮 Маги",
                "marksmen": "🏹 Стрільці",
                "supports": "💖 Сапорти"
            },
            "heroes": {
                "classes": {
                    "tank": {
                        "name": "Танки",
                        "heroes": ["Тигріл", "Франко", "Джонсон"]
                    },
                    "fighter": {
                        "name": "Файтери",
                        "heroes": ["Балмонд", "Зілонг", "Руби"]
                    }
                    # Add other classes
                }
            }
        }
