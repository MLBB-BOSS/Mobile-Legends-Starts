from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from utils.charts import generate_rating_chart
from services.user_service import get_user_profile_text, update_mlbb_id

profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession):
    profile_text = await get_user_profile_text(db, message.from_user.id)

    if not profile_text:
        profile_text = "🔎 <b>Профіль не знайдено або ще не заповнено.</b>"

    # Генерація графіку
    chart_bytes = generate_rating_chart([100, 120, 140, 180, 210, 230])
    input_file = BufferedInputFile(chart_bytes.read(), filename='rating_chart.png')

    await message.answer_photo(photo=input_file, caption=profile_text)

@profile_router.message(Command("add_mlbb"))
async def add_mlbb_id(message: Message, db: AsyncSession):
    args = message.get_args()
    if not args.isdigit():
        await message.answer("🚨 Некоректний MLBB ID. Спробуйте ще раз!")
        return

    response = await update_mlbb_id(db, message.from_user.id, args)
    await message.answer(response)
