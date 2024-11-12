# handlers/base_handler.py
from abc import ABC, abstractmethod
from typing import Any, Optional
from telegram import Update
from telegram.ext import ContextTypes
from database.connection import db

class BaseHandler(ABC):
    def __init__(self):
        self._error_messages = {
            'not_found': 'Запитаний ресурс не знайдено',
            'permission_denied': 'У вас немає прав для виконання цієї дії',
            'invalid_input': 'Невірний формат введених даних'
        }

    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE, error: Exception) -> None:
        """Обробка помилок"""
        error_message = str(error) or self._error_messages.get('general', 'Сталася помилка')
        if update.effective_message:
            await update.effective_message.reply_text(f"❌ {error_message}")

    @abstractmethod
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        """Абстрактний метод обробки команди"""
        pass

    async def validate_user(self, update: Update) -> bool:
        """Перевірка прав користувача"""
        with db.get_session() as session:
            user = session.query(User).filter(
                User.telegram_id == update.effective_user.id
            ).first()
            return user is not None
