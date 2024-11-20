# handlers/error_handler.py
from aiogram import Router
from aiogram.types import ErrorEvent
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def error_handler(event: ErrorEvent):
    try:
        # Отримуємо інформацію про помилку
        error = event.exception
        update = event.update
        
        # Логуємо помилку
        logger.error(f"Помилка при обробці оновлення {update}: {error}")
        
        # Якщо є чат, відправляємо повідомлення про помилку
        if hasattr(update, 'message') and update.message:
            await update.message.answer(
                "Вибачте, сталася помилка при обробці вашого запиту. "
                "Спробуйте пізніше або зверніться до адміністратора."
            )
    except Exception as e:
        logger.error(f"Помилка в обробнику помилок: {e}")
