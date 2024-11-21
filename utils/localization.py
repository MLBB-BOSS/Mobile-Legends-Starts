# File: utils/localization.py

import json
import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class Localization:
    def __init__(self, default_language: str = "uk"):
        self.default_language = default_language
        self.messages: Dict[str, Any] = {}
        self._load_messages()

    def _load_messages(self) -> None:
        try:
            # Update the path to match your project structure
            locale_path = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "config",
                "messages",
                "locales",
                f"{self.default_language}.json"
            )
            with open(locale_path, 'r', encoding='utf-8') as file:
                self.messages = json.load(file)
            logger.info(f"Loaded messages for language: {self.default_language}")
        except Exception as e:
            logger.error(f"Failed to load messages: {e}")
            self.messages = {}

    def get_message(self, key: str) -> str:
        """Get message by dot-separated key path"""
        try:
            value = self.messages
            for k in key.split('.'):
                value = value[k]
            return str(value)
        except (KeyError, TypeError) as e:
            logger.error(f"Missing localization key: {key}, Error: {e}")
            return key

# Global instance
loc = Localization()
