import json
from pathlib import Path
import logging

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.messages = self._load_messages()
        self.logger = logging.getLogger(__name__)

    def _load_messages(self) -> dict:
        try:
            base_path = Path(__file__).parent.parent
            file_path = base_path / "utils" / "messages" / f"{self.locale}.json"
            
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            self.logger.error(f"Error loading messages: {e}")
            return {}

    def get_message(self, key: str, **kwargs) -> str:
        """
        Отримати повідомлення за ключем
        Приклад: loc.get_message("messages.welcome")
        """
        try:
            keys = key.split('.')
            value = self.messages
            for k in keys:
                value = value.get(k, {})
            
            if isinstance(value, str):
                return value.format(**kwargs)
            return key
        except Exception as e:
            self.logger.error(f"Error getting message for key {key}: {e}")
            return key

# Створюємо глобальний екземпляр
loc = LocalizationManager()
