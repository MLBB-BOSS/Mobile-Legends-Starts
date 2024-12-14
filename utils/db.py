# utils/db.py
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.user import User, Badge
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
    # Використовуємо selectinload для жадного завантаження бейджів
    stmt = (
        select(User)
        .where(User.telegram_id == telegram_id)
        .options(selectinload(User.badges))
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_all_badges(db: AsyncSession) -> list[Badge]:
    stmt = select(Badge)
    result = await db.execute(stmt)
    return result.scalars().all()