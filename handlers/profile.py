from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.orm import Session
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
        # Отримати асинхронну сесію БД
        db_session = await get_db_session()  
        data["db"] = db_session
        return await handler(event, data)

profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: Session):
    # Отримати текст профілю користувача
    profile_text = await get_user_profile_text(db, message.from_user.id)

    # Фіктивна історія рейтингу (для прикладу)
    rating_history = [100, 120, 140, 180, 210, 230]

    # Згенерувати графік рейтингу (повертає BytesIO)
    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)

    # Створити BufferedInputFile з байтових даних
    input_file = BufferedInputFile(
        chart_bytes.read(),
        filename='chart.png'
    )

    # Надіслати зображення користувачеві
    await message.answer_photo(photo=input_file, caption=profile_text)
