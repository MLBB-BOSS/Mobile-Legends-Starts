import json
from pathlib import Path
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logger = logging.getLogger(__name__)

class LocalizationManager:
    def __init__(self, locale: str = "uk"):
        self.locale = locale
        self.messages = self._load_messages()

    def _load_messages(self) -> dict:
        try:
            file_path = Path(__file__).parent.parent / "config" / "messages" / "locales" / f"{self.locale}.json"
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
                        logger.warning(f"Ключ не знайдено: {key}")
                        return key
                else:
                    break
            if isinstance(current, str):
                return current.format(**kwargs)
            elif isinstance(current, (list, dict)):
                return str(current)
            return key
        except Exception as e:
            logger.error(f"Помилка отримання повідомлення для ключа {key}: {e}")
            return key

    def get_hero_classes(self) -> list:
        try:
            classes = self.messages.get("heroes", {}).get("classes", {})
            return list(classes.keys()) if isinstance(classes, dict) else []
        except Exception as e:
            logger.error(f"Помилка отримання списку класів героїв: {e}")
            return []

    def get_hero_info(self, hero_name: str) -> str:
        try:
            return self.messages.get("heroes", {}).get("info", {}).get(hero_name, self.get_message("errors.hero_not_found"))
        except Exception as e:
            logger.error(f"Помилка отримання інформації про героя {hero_name}: {e}")
            return self.get_message("errors.general")

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="buttons.guides"),
                    KeyboardButton(text="buttons.characters")
                ],
                [
                    KeyboardButton(text="buttons.counter_picks"),
                    KeyboardButton(text="buttons.builds")
                ],
                [
                    KeyboardButton(text="buttons.back")
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    def get_builds_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="buttons.build1"),
                    KeyboardButton(text="buttons.build2")
                ],
                [
                    KeyboardButton(text="buttons.back_to_navigation")
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
