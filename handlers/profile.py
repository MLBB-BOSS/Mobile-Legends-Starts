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
        try:
            return await handler(event, data)
        finally:
            await db_session.close()


# Створюємо роутер для профілю
profile_router = Router()
profile_router.message.middleware(DbSessionMiddleware())


# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: Session):
    profile_text = await get_user_profile_text(db, message.from_user.id)

    if not profile_text or not profile_text.strip():
        profile_text = "🔎 <b>Профіль не знайдено або ще не заповнено.</b>\nСкористайтесь іншими командами для його налаштування."

    rating_history = [100, 120, 140, 180, 210, 230]
    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)

    input_file = BufferedInputFile(
        chart_bytes.read(),
        filename='rating_chart.png'
    )

    await message.answer_photo(photo=input_file, caption=profile_text)


# Обробник для команди /add_mlbb
@profile_router.message(Command("add_mlbb"))
async def add_mlbb_id(message: Message, db: Session):
    args = message.get_args()
    if not args or not args.strip().isdigit():
        await message.answer("🚨 <b>Некоректний ввід!</b>\nБудь ласка, введіть ваш MLBB ID у форматі:\n<code>/add_mlbb 123456789</code>")
        return
    
    response = await update_mlbb_id(db, message.from_user.id, args.strip())
    await message.answer(response)
