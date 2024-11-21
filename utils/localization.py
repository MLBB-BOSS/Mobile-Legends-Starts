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
            # Вказуємо правильний шлях до файлу локалізації
            file_path = Path(__file__).parent / "messages" / f"{self.locale}.json"

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
        """
        Отримати локалізоване повідомлення за ключем
        Приклад: get_message("messages.welcome")
        """
        try:
            current = self.messages
            for part in key.split('.'):
                if isinstance(current, dict):
                    current = current.get(part)
                    if current is None:
                        if key != "messages.errors.general":
                            logger.warning(f"Ключ не знайдено: {key}")
                            # Повертаємо повідомлення про загальну помилку без рекурсії
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
        """Отримати список класів героїв"""
        try:
            classes = self.messages.get("heroes", {}).get("classes", {})
            return list(classes.keys()) if isinstance(classes, dict) else []
        except Exception as e:
            logger.error(f"Помилка отримання списку класів героїв: {e}")
            return []

    def get_all_hero_names(self) -> list:
        """Отримати список усіх імен героїв"""
        try:
            heroes_info = self.messages.get('heroes', {}).get('info', {})
            return list(heroes_info.keys())
        except Exception as e:
            logger.error(f"Помилка отримання списку імен героїв: {e}")
            return []

    def get_hero_info(self, hero_name: str) -> str:
        """Отримати інформацію про героя"""
        try:
            return self.messages.get("heroes", {}).get("info", {}).get(hero_name, 
                   self.get_message("messages.errors.hero_not_found"))
        except Exception as e:
            logger.error(f"Помилка отримання інформації про героя {hero_name}: {e}")
            return self.get_message("messages.errors.general")

# Створюємо глобальний екземпляр
loc = LocalizationManager()
