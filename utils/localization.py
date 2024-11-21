# utils/localization.py

import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.messages = self._load_messages()

    def _load_messages(self) -> dict:
        try:
            # Оновлюємо шлях до файлу локалізації
            base_path = Path(__file__).parent.parent  # Піднімаємося на рівень вище від 'utils'
            file_path = base_path / "config" / "messages" / "locales" / f"{self.locale}.json"

            if not file_path.exists():
                logger.error(f"Файл локалізації не знайдено: {file_path}")
                return {}

            with open(file_path, 'r', encoding='utf-8') as file:
                messages = json.load(file)
                logger.info(f"Локалізація успішно завантажена: {self.locale}")
                return messages

        except json.JSONDecodeError as e:
            logger.error(f"Помилка декодування JSON: {e}")
            return {}
        except Exception as e:
            logger.error(f"Помилка завантаження локалізації: {e}")
            return {}

    def get_message(self, key: str, **kwargs) -> str:
        try:
            current = self.messages
            for part in key.split('.'):
                if isinstance(current, dict):
                    current = current.get(part)
                    if current is None:
                        if key != "messages.errors.general":
                            logger.warning(f"Ключ не знайдено: {key}")
                            return self.messages.get("messages", {}).get("errors", {}).get("general", "Сталася непередбачена помилка.")
                        else:
                            logger.error(f"Ключ не знайдено: {key}")
                            return "Сталася непередбачена помилка."
                else:
                    break

            if isinstance(current, str):
                return current.format(**kwargs)
            elif isinstance(current, (list, dict)):
                return str(current)
            return self.messages.get("messages", {}).get("errors", {}).get("general", "Сталася непередбачена помилка.")

        except Exception as e:
            logger.error(f"Помилка отримання повідомлення для ключа {key}: {e}")
            return "Сталася непередбачена помилка."

    def get_hero_classes(self) -> list:
        try:
            classes = self.messages.get("heroes", {}).get("classes", {})
            return list(classes.keys()) if isinstance(classes, dict) else []
        except Exception as e:
            logger.error(f"Помилка отримання списку класів героїв: {e}")
            return []

    def get_all_hero_names(self) -> list:
        try:
            heroes_info = self.messages.get('heroes', {}).get('info', {})
            return list(heroes_info.keys())
        except Exception as e:
            logger.error(f"Помилка отримання списку імен героїв: {e}")
            return []

    def get_hero_info(self, hero_name: str) -> str:
        try:
            return self.messages.get("heroes", {}).get("info", {}).get(hero_name,
                   self.get_message("messages.errors.hero_not_found"))
        except Exception as e:
            logger.error(f"Помилка отримання інформації про героя {hero_name}: {e}")
            return self.get_message("messages.errors.general")

# Створюємо глобальний екземпляр
loc = LocalizationManager()
