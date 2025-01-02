from aiogram import Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.orm import Session
from io import BytesIO

# Імпортуємо функцію для отримання асинхронної сесії БД
from utils.db import get_db_session

# Сервіс отримання тексту профілю (запити до БД)
from services.user_service import get_user_profile_text

# Функція для генерування графіка у форматі BytesIO
from utils.charts import generate_rating_chart


class DbSessionMiddleware(BaseMiddleware):
    """
    Проміжна ланка (middleware), яка створює 
    та додає об'єкт сесії БД у словник data для використання в хендлерах.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Отримуємо асинхронну сесію БД
        db_session = await get_db_session()
        data["db"] = db_session
        return await handler(event, data)


# Створюємо окремий роутер для обробників профілю
profile_router = Router()

# Додаємо middleware для всіх message-хендлерів у цьому роутері
profile_router.message.middleware(DbSessionMiddleware())


@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: Session):
    """
    Хендлер на команду /profile: 
    - отримує текст профілю користувача з БД,
    - генерує графік у пам'яті (BytesIO),
    - відправляє його користувачеві як фото.
    """
    # Отримати текст профілю користувача
    profile_text = await get_user_profile_text(db, message.from_user.id)

    # Фіктивна історія рейтингу для прикладу
    rating_history = [100, 120, 140, 180, 210, 230]

    # Генеруємо графік рейтингу (функція повертає BytesIO)
    chart_bytes = generate_rating_chart(rating_history)
    chart_bytes.seek(0)  # Переміщаємо "курсор" на початок

    # Створюємо BufferedInputFile із байтових даних
    input_file = BufferedInputFile(
        chart_bytes.read(),
        filename='chart.png'
    )

    # Відправляємо зображення користувачеві з підписом
    await message.answer_photo(photo=input_file, caption=profile_text)
