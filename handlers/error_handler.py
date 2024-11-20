# handlers/error_handler.py
from aiogram import Router, types
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramAPIError
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def errors_handler(event: ErrorEvent) -> None:
    """
    Обробник помилок для aiogram 3.x
    """
    try:
        # Отримуємо update та exception з події
        update = event.update
        exception = event.exception
        
        # Логуємо помилку
        logger.error(f"Помилка при обробці оновлення {update}: {exception}")

        # Визначаємо chat_id
        chat_id = None
        if update.message:
            chat_id = update.message.chat.id
        elif update.callback_query:
            chat_id = update.callback_query.message.chat.id

        if chat_id:
            # Визначаємо тип помилки та відповідне повідомлення
            if isinstance(exception, TelegramAPIError):
                error_message = loc.get_message("errors.telegram_api")
            else:
                error_message = loc.get_message("errors.general")

            # Відправляємо повідомлення про помилку
            await event.update.bot.send_message(
                chat_id=chat_id,
                text=error_message
            )
            
    except Exception as e:
        logger.error(f"Помилка в обробнику помилок: {e}")
