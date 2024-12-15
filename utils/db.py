import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.badge import Badge
from models.user_badges import user_badges

# Отримання бейджів користувача
async def get_user_badges(session: AsyncSession, user_id: int):
    """
    Отримує всі бейджі користувача за його user_id.
    """
    query = (
        select(Badge)
        .join(user_badges, Badge.id == user_badges.c.badge_id)
        .where(user_badges.c.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().all()


# URL бази даних — використовуйте змінну середовища для безпеки
AS_BASE = os.getenv(
    "AS_BASE",
    "postgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd"
)

if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid. Please configure your database connection.")

# Ініціалізація асинхронного двигуна для роботи з базою даних
engine = create_async_engine(AS_BASE, echo=True)  # echo=True для налагодження, вимкніть у продакшені
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Функція для отримання сесії
async def get_db_session() -> AsyncSession:
    """
    Повертає сесію бази даних.
    """
    async with async_session() as session:
        yield session
