import json
from pathlib import Path

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.messages = self._load_messages()

    def _load_messages(self) -> dict:
        try:
            base_path = Path(__file__).parent.parent
            file_path = base_path / "config" / "messages" / "locales" / f"{self.locale}.json"

            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading messages: {e}")
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
                value = value.get(k)
                if value is None:
                    return key  # Return the key if not found

            if isinstance(value, str):
                return value.format(**kwargs)
            else:
                return value
        except Exception as e:
            print(f"Error getting message for key {key}: {e}")
            return key

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
            return hero_names
        except Exception as e:
            print(f"Error getting all hero names: {e}")
            return []

# Створюємо глобальний екземпляр
loc = LocalizationManager()
