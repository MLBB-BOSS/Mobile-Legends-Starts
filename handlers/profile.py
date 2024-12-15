from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO
from utils.db import get_db_session, get_user_badges
from services.user_service import get_user_profile_text
from utils.charts import generate_rating_chart
import logging

logger = logging.getLogger(__name__)

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """
        Middleware для створення та закриття сесії бази даних.
        """
        db_session = await get_db_session()
        data["db"] = db_session
        try:
            return await handler(event, data)
        finally:
            await db_session.close()

profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession):
    """
    Відображає профіль користувача, включаючи текстовий опис, бейджі та графік рейтингу.
    """
    try:
        # Отримуємо текст профілю та історію рейтингу
        profile_data = await get_user_profile_text(db, message.from_user.id, message.from_user.username)

        if not isinstance(profile_data, dict) or "text" not in profile_data:
            raise ValueError("Invalid profile data format")

        profile_text = profile_data["text"]
        rating_history = profile_data.get("rating_history", [100, 120, 140, 180, 210, 230])

        if not rating_history:
            rating_history = [100]  # Значення за замовчуванням

        # Отримуємо бейджі користувача
        badges = await get_user_badges(db, message.from_user.id) or []
        badge_names = [badge.name for badge in badges]
        profile_text += f"\n🏅 Бейджі: {', '.join(badge_names) if badge_names else 'Немає'}"

        # Генеруємо графік рейтингу
        chart_bytes = generate_rating_chart(rating_history)
        chart_bytes.seek(0)

        # Створюємо BufferedInputFile з байтових даних
        input_file = BufferedInputFile(
            chart_bytes.read(),
            filename='chart.png'
        )

        # Відправляємо текстовий профіль та графік
        await message.answer_photo(photo=input_file, caption=profile_text)
    except Exception as e:
        logger.error(f"Error while generating profile for user {message.from_user.id}: {e}")
        await message.answer("⚠️ Виникла помилка при отриманні вашого профілю. Спробуйте пізніше.")
        raise
