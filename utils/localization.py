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
            base_path = Path(__file__).parent.parent  # Піднімаємося на рівень вище
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

    # Інші методи залишаються без змін

# Створюємо глобальний екземпляр
loc = LocalizationManager()
