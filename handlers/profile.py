from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.orm import Session
from io import BytesIO

from utils.db import get_db_session
from services.user_service import get_user_profile_text, update_mlbb_id
from utils.charts import generate_rating_chart


# Middleware для отримання сесії бази даних
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


# Створюємо роутер для профілю
profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())


# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: Session):
    # Отримуємо текст профілю користувача
    profile_text = await get_user_profile_text(db, message.from_user.id)

    # Фіктивна історія рейтингу (тестові дані для графіку)
    rating_history = [100, 120, 140, 180, 210, 230]

    # Генеруємо графік рейтингу у вигляді BytesIO
    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)

    # Створюємо BufferedInputFile для Telegram
    input_file = BufferedInputFile(
        chart_bytes.read(),
        filename='rating_chart.png'
    )

    # Відправляємо графік користувачу разом із текстом профілю
    await message.answer_photo(photo=input_file, caption=profile_text)


# Обробник для команди /add_mlbb
@profile_router.message(Command("add_mlbb"))
async def add_mlbb_id(message: Message, db: Session):
    args = message.get_args()
    if not args:
        await message.answer("Будь ласка, введіть ваш MLBB ID: /add_mlbb <ваш_id>")
        return
    
    response = await update_mlbb_id(db, message.from_user.id, args)
    await message.answer(response)
