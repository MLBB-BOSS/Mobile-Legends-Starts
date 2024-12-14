from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.user_service import get_user_profile_text
from utils.charts import generate_rating_chart

profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db):
    # Отримуємо текст профілю
    profile_text = await get_user_profile_text(db, message.from_user.id)
    
    # Тут ви можете отримати історію рейтингу користувача (наприклад з БД)
    # Для прикладу візьмемо якусь фіктивну історію
    rating_history = [100, 120, 140, 180, 210, 230]

    chart = generate_rating_chart(rating_history)
    
    # Відправляємо профіль та графік
    await message.answer_photo(photo=chart, caption=profile_text)
