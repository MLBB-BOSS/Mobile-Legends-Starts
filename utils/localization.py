# File: utils/localization.py

import json
from pathlib import Path
import logging

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.logger = logging.getLogger(__name__)
        self.messages = self._load_messages()
        if not self.messages:
            self.logger.error(f"No messages loaded for locale '{self.locale}'")

    def _load_messages(self) -> dict:
        try:
            base_path = Path(__file__).parent.parent
            file_path = base_path / "messages" / f"{self.locale}.json"

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
        """
        Отримати повідомлення за ключем
        Приклад: loc.get_message("messages.welcome")
        """
        try:
            keys = key.split('.')
            value = self.messages
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    self.logger.warning(f"Expected dict at key '{k}' but got {type(value)}")
                    return f"Message key '{key}' not found"

                if value is None:
                    self.logger.warning(f"Message key '{key}' not found at '{k}'")
                    return f"Message key '{key}' not found"

            if isinstance(value, str):
                return value.format(**kwargs)
            elif isinstance(value, dict):
                return value
            else:
                self.logger.warning(f"Unsupported type for key '{key}': {type(value)}")
                return f"Message key '{key}' not found"
        except KeyError as e:
            self.logger.error(f"Missing key in localization for '{key}': {e}")
            return f"Error getting message for key '{key}'"
        except Exception as e:
            self.logger.error(f"Error getting message for key {key}: {e}")
            return f"Error getting message for key '{key}'"

    def get_all_hero_names(self) -> list:
        """
        Повертає список всіх імен героїв з локалізації
        """
        try:
            hero_classes = self.get_message("heroes.classes")
            hero_names = []
            if isinstance(hero_classes, dict):
                for class_info in hero_classes.values():
                    heroes = class_info.get("heroes", [])
                    hero_names.extend(heroes)
            else:
                self.logger.warning("heroes.classes is not a dictionary")
            return hero_names
        except Exception as e:
            self.logger.error(f"Error getting all hero names: {e}")
            return []

# Створюємо глобальний екземпляр
loc = LocalizationManager()
logger = logging.getLogger(__name__)
logger.info(f"Значення 'buttons.profile': {loc.get_message('buttons.profile')}")
logger.info(f"Значення 'messages.unhandled_message': {loc.get_message('messages.unhandled_message', message='Тестове повідомлення')}")
