# File: utils/localization.py

import json
import os
import logging
from typing import Optional, Any, Dict

logger = logging.getLogger(__name__)

class Localization:
    def __init__(self, default_language: str = "uk"):
        self.default_language = default_language
        self.messages: Dict[str, Dict[str, Any]] = {}
        self._load_messages()

    def _load_messages(self) -> None:
        """Load messages from JSON files in the locales directory"""
        try:
            locale_path = os.path.join(os.path.dirname(__file__), "..", "locales", f"{self.default_language}.json")
            with open(locale_path, 'r', encoding='utf-8') as file:
                self.messages = json.load(file)
            logger.info(f"Loaded messages for language: {self.default_language}")
        except Exception as e:
            logger.error(f"Failed to load messages: {e}")
            self.messages = self._get_default_messages()

    def _get_default_messages(self) -> Dict[str, Dict[str, str]]:
        """Return default messages in case the locale file fails to load"""
        return {
            "messages": {
                "welcome": "Вітаємо в MLBB BOSS! 🎮",
                "unhandled_message": "Вибачте, я не розумію це повідомлення: {message_text}",
                "error": "Виникла помилка. Спробуйте ще раз пізніше."
            },
            "buttons": {
                "navigation": "📍 Навігація",
                "profile": "👤 Профіль",
                "settings": "⚙️ Налаштування",
                "help": "❓ Допомога",
                "back": "↩️ Назад"
            }
        }

    def get_message(self, key: str, **kwargs) -> str:
        """
        Get a message by its key with optional formatting parameters
        
        Args:
            key: The dot-separated path to the message
            **kwargs: Format parameters for the message
        
        Returns:
            The formatted message string
        """
        try:
            # Split the key into parts (e.g., "messages.welcome" -> ["messages", "welcome"])
            parts = key.split('.')
            
            # Navigate through the nested dictionary
            message = self.messages
            for part in parts:
                message = message[part]

            # If the message is None or empty, raise KeyError
            if not message:
                raise KeyError(f"Empty message for key: {key}")

            # Try to format the message with the provided kwargs
            try:
                return message.format(**kwargs)
            except KeyError as e:
                logger.error(f"Missing format parameter in message {key}: {e}")
                return message  # Return unformatted message as fallback
            except Exception as e:
                logger.error(f"Error formatting message {key}: {e}")
                return message  # Return unformatted message as fallback
                
        except KeyError as e:
            logger.error(f"Missing message key: {key}")
            return self._get_default_messages()["messages"]["error"]
        except Exception as e:
            logger.error(f"Error getting message {key}: {e}")
            return self._get_default_messages()["messages"]["error"]

# Create a global instance
loc = Localization()
