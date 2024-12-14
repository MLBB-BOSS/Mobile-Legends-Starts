# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User, Badge
from database import async_session

async def get_db_session() -> AsyncSession:
    """
    Повертає нову асинхронну сесію для роботи з базою даних.
    Оскільки async_session – це sessionmaker, виклик async_session() поверне екземпляр AsyncSession.
    Це не корутина, тому не треба await при виклику async_session().
    
    Якщо в коді використовується await get_db_session(), переконайтеся, що ви усуваєте await.
    Просто викликайте session = await get_db_session() якщо вам конче потрібен await, але у цьому випадку
    функція проста і не містить await всередині, тож можна опустити await у місцях де вона викликається.
    
    Найкраще: викликати session = await get_db_session() все одно працюватиме, бо функція async,
    але всередині нема корутин. Для консистентності залишимо async.
    """
    # Оскільки async_session - це sessionmaker,
    # async_session() створює новий AsyncSession.
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