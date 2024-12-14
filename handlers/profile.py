# handlers/profile.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import get_user_profile_text
from utils.charts import generate_rating_chart

profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession):
    # Викликаємо функцію, яка створить або отримає профіль
    profile_text = await get_user_profile_text(db, message.from_user.id, message.from_user.username or "")
    rating_history = [100, 120, 140, 180, 210, 230]  # Приклад даних для графіка

    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)
    input_file = BufferedInputFile(chart_bytes.read(), filename='chart.png')

    await message.answer_photo(photo=input_file, caption=profile_text)