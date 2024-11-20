# handlers/message_handlers.py
from aiogram import Router, F
from aiogram.types import Message
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def handle_message(message: Message):
    try:
        # Перевіряємо чи message.dict() повертає словник
        message_dict = message.model_dump() if hasattr(message, 'model_dump') else {}
        
        if not isinstance(message_dict, dict):
            logger.error(f"Неочікуваний тип даних повідомлення: {type(message_dict)}")
            return
            
        # Безпечно отримуємо значення
        text = message.text if message.text else ""
        
        # Логуємо отримане повідомлення
        logger.info(f"Отримано повідомлення: {text[:100]}")
        
        # Обробка повідомлення
        await handle_user_message(message)
        
    except AttributeError as e:
        logger.error(f"Помилка доступу до атрибуту: {e}")
    except Exception as e:
        logger.error(f"Помилка при обробці повідомлення: {e}")

async def handle_user_message(message: Message):
    """Обробка користувацького повідомлення"""
    try:
        if not message.text:
            return
            
        # Базова обробка текстових повідомлень
        text = message.text.lower()
        
        # Тут додайте вашу логіку обробки повідомлень
        if text == "меню":
            await message.answer("Головне меню:")
            # Додайте відображення меню
        elif text.startswith("/"):
            # Ігноруємо команди, вони обробляються іншими хендлерами
            return
        else:
            # Обробка звичайних повідомлень
            await message.answer("Отримано ваше повідомлення")
            
    except Exception as e:
        logger.error(f"Помилка в handle_user_message: {e}")
        await message.answer("Вибачте, сталася помилка при обробці вашого повідомлення")
