from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO

from utils.db import get_db_session
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
    Відображає профіль користувача, включаючи текстовий опис та графік рейтингу.
    """
    # Отримуємо текст профілю
    profile_text = await get_user_profile_text(db, message.from_user.id)

    # Генеруємо графік рейтингу (фіктивна історія, замінити на реальні дані)
    stats = await get_user_profile_text(db, message.from_user.id)
    rating_history = stats.get("rating_history", [100, 120, 140, 180, 210, 230])  # Заглушка

    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)

    input_file = BufferedInputFile(
        chart_bytes.read(),
        filename='chart.png'
    )

    # Надсилаємо текстовий профіль та графік
    await message.answer_photo(photo=input_file, caption=profile_text)
