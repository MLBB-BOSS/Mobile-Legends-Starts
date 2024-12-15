from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO

from utils.db import get_db_session, get_user_badges
from services.user_service import get_user_profile_text
from utils.charts import generate_rating_chart

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        db_session = await get_db_session()
        data["db"] = db_session
        return await handler(event, data)

profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession):
    """
    Відображає профіль користувача, включаючи текстовий опис, бейджі та графік рейтингу.
    """
    # Отримуємо текст профілю
    profile_data = await get_user_profile_text(db, message.from_user.id)
    profile_text = profile_data["text"]  # Текстовий профіль
    rating_history = profile_data.get("rating_history", [100, 120, 140, 180, 210, 230])  # Історія рейтингу

    # Отримуємо бейджі користувача
    badges = await get_user_badges(db, message.from_user.id)
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
