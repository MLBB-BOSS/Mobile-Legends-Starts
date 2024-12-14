# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import Badge, User

async def get_all_badges(db: AsyncSession):
    """
    Повертає список усіх бейджів, доступних у боті.
    Це бейджі, які можуть бути присвоєні, але не обов'язково вже присвоєні користувачам.
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
