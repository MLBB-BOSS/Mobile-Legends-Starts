from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# URL бази даних
AS_BASE = os.getenv("AS_BASE", "your_default_connection_string")
if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid")

# Ініціалізація асинхронного двигуна
engine = create_async_engine(AS_BASE, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_user_badges(session, user_id):
    """
    Отримує всі бейджі користувача. 
    Імпортуємо Badge локально, щоб уникнути циклічного імпорту.
    """
    from models.badge import Badge  # Локальний імпорт
    from models.user_badges import user_badges
    from sqlalchemy import select

    query = (
        select(Badge)
        .join(user_badges, Badge.id == user_badges.c.badge_id)
        .where(user_badges.c.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().all()