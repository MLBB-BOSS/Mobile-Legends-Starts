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
