from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.orm import Session
from io import BytesIO
import logging

from utils.db import get_db_session
from services.user_service import get_user_profile_text
from utils.charts import generate_rating_chart

# Налаштування логування
logging.basicConfig(level=logging.INFO)

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: Dict[str, Any]
    ) -> Any:
        # Отримати асинхронну сесію БД
        db_session = await get_db_session()
        data["db"] = db_session
        return await handler(event, data)

profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: Session):
    try:
        # Отримати текст профілю користувача
        profile_text = await get_user_profile_text(
            db, 
            message.from_user.id, 
            message.from_user.username or "Невідомий користувач"
        )
        logging.info(f"Текст профілю отримано: {profile_text}")

        # Фіктивна історія рейтингу
        rating_history = [100, 120, 140, 180, 210, 230]

        if not rating_history:
            await message.answer("Дані для графіка порожні!")
            return

        # Генерувати графік рейтингу
        chart_bytes = generate_rating_chart(rating_history)
        logging.info("Графік успішно згенерований")

        # Створити BufferedInputFile з байтових даних
        input_file = BufferedInputFile(
            chart_bytes.read(),
            filename='chart.png'
        )

        # Надіслати зображення користувачеві
        await message.answer_photo(photo=input_file, caption=profile_text)

    except Exception as e:
        logging.error(f"Загальна помилка у обробнику /profile: {e}")
        await message.answer("Сталася помилка при обробці запиту.")