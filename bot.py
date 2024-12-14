# services/user_service.py
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models.user import User
from models.user_stats import UserStats
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str) -> User:
    try:
        stmt = select(User).options(joinedload(User.stats), joinedload(User.badges)).where(User.telegram_id == telegram_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            user = User(telegram_id=telegram_id, username=username)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"Створено нового користувача з telegram_id={telegram_id}")
        else:
            # Завантажуємо статистику та бейджі разом з користувачем
            await db.refresh(user, attribute_names=["stats", "badges"])

        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_or_create_user: {e}")
        await db.rollback()
        raise