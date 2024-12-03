# keyboards/ai_menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
from keyboards.menus import MenuButton  # Імпортуємо MenuButton для використання кнопки "🔙"

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_ai_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Створює меню для розділу AI.
    """
    buttons = [
        KeyboardButton(text="🤖 Запитати AI"),
        KeyboardButton(text="📚 Інструкції"),
        KeyboardButton(text=MenuButton.BACK.value)  # Кнопка "🔙"
    ]
    keyboard = [
        buttons  # Розміщуємо всі кнопки в одному рядку
    ]
    logger.info(f"Створення AI меню з кнопками: {[button.text for button in buttons]}")
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
