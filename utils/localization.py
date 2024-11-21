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
                return current.format(**kwargs)
            return str(current)
        except KeyError:
            logger.error(f"Missing localization key: {key}")
            return key
        except Exception as e:
            logger.error(f"Error getting message for key {key}: {str(e)}")
            return key

    def _get_default_messages(self) -> Dict[str, Any]:
        return {
            "messages": {
                "unhandled_message": "Вибачте, я не розумію команду: {text}",
                "welcome": "Ласкаво просимо до MLS Bot!",
                "error": "Виникла помилка. Спробуйте ще раз.",
            },
            "buttons": {
                "navigation": "📱 Навігація",
                "characters": "👥 Герої",
                "back": "↩️ Назад",
            }
        }

# Create a singleton instance
loc = Localization()

# Export both the class and the singleton instance
__all__ = ['Localization', 'loc']
