import json
from pathlib import Path
import logging

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.logger = logging.getLogger(__name__)
        self.messages = self._load_messages()

    def _load_messages(self) -> dict:
        try:
            file_path = Path(__file__).parent.parent / "locales" / f"{self.locale}.json"
            with open(file_path, "r", encoding="utf-8") as file:
                messages = json.load(file)
                self.logger.info(f"Localization file loaded: {file_path}")
                return messages
        except FileNotFoundError:
            self.logger.error(f"Localization file not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {file_path}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Error loading messages: {e}")
            return {}

    def get_message(self, key: str, **kwargs) -> str:
        try:
            keys = key.split('.')
            value = self.messages
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return f"Message key '{key}' not found"
                if value is None:
                    return f"Message key '{key}' not found"

            if isinstance(value, str):
                return value.format(**kwargs)
            return value
        except Exception as e:
            self.logger.error(f"Error getting message for key {key}: {e}")
            return f"Error getting message for key '{key}'"

# Ініціалізація
loc = LocalizationManager(locale="uk")
