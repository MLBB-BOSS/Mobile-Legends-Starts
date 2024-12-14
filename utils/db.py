# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User, Badge
from database import async_session

async def get_db_session() -> AsyncSession:
    """
    Повертає нову асинхронну сесію для роботи з базою даних.
    Використовується, якщо ви не застосовуєте middleware для сесій.
    Якщо ви застосовуєте middleware, ця функція може не знадобитися.
    """
    # Якщо ви хочете повертати контекстний менеджер, це буде async generator,
    # але зараз просто повернемо екземпляр сесії.
    # Попередження: Викликати await get_db_session() при кожному використанні може бути не найкраща ідея,
    # краще використовувати middleware або інший підхід. Це спрощений приклад.
    return async_session()

async def get_all_badges(db: AsyncSession):
    """
    Повертає список усіх бейджів, доступних у боті.
    """
    result = await db.execute(select(Badge))
    badges = result.scalars().all()
    return badges

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User:
    """
    Отримує користувача за telegram_id.
    Повертає об’єкт User або None, якщо користувача не знайдено.
    """
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()
    return user