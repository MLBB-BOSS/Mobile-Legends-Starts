# utils/localization.py
import json
import os
from typing import Any

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.messages = self._load_messages()

    def _load_messages(self) -> dict:
        file_path = os.path.join("config", "messages", "locales", f"{self.locale}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading messages: {e}")
            return {}

    def get_message(self, key: str, **kwargs) -> str:
        """
        Get message by key with formatting
        Example: loc.get_message("messages.welcome")
        """
        keys = key.split('.')
        value = self.messages
        for k in keys:
            value = value.get(k, {})
        
        if isinstance(value, str):
            return value.format(**kwargs)
        return key

loc = LocalizationManager()
