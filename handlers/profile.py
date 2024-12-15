from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.orm import Session
from io import BytesIO

from utils.db import get_db_session  # Імпорт функції отримання сесії БД
from services.user_service import get_user_profile_text  # Функція для отримання тексту профілю
from utils.charts import generate_rating_chart  # Функція для генерації графіка

# Ініціалізація роутера для обробки профілю
profile_router = Router()

@profile_router.message(Command("profile"))
async def show_profile(message: Message):
    """Команда для показу профілю користувача"""
    # Отримання сесії БД
    async with get_db_session() as db:
        # Отримати текст профілю користувача
        profile_text = await get_user_profile_text(db, message.from_user.id)

        # Дані для графіка (приклад)
        rating_history = [100, 120, 140, 180, 210, 230]  # Можна замінити реальними даними

        # Генерація графіка
        chart_bytes = generate_rating_chart(rating_history)
        chart_bytes.seek(0)

        # Підготовка графіка як BufferedInputFile
        input_file = BufferedInputFile(
            chart_bytes.read(),
            filename='rating_chart.png'
        )

        # Форматований текст профілю
        profile_caption = (
            f"📊 *Ваш профіль гравця*\n\n"
            f"🏆 Загальний рейтинг: *230*\n"
            f"📝 _Ваші досягнення:_\n"
            f"- Перемог: *42*\n"
            f"- Поразок: *18*\n"
            f"- Найкращий герой: *Ланселот*\n\n"
            f"[Детальніше про вашу статистику](https://example.com/profile)"
        )

        # Надсилання графіка разом із текстом
        await message.answer_photo(photo=input_file, caption=profile_caption, parse_mode="Markdown")
