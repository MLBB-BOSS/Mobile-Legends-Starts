import json
from pathlib import Path

class Localization:
    def __init__(self, lang: str = "uk"):
        self.lang = lang
        self.messages = self.load_messages()

    def load_messages(self):
        """
        Завантажує JSON-файл з повідомленнями для вказаної мови.
        """
        file_path = Path(f"config/messages/{self.lang}.json")
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def get_message(self, key: str) -> str:
        """
        Отримує повідомлення за ключем.
        """
        return self.messages.get(key, "Повідомлення не знайдено.")
