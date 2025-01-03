# utils/db.py
from sqlalchemy.future import select
from .models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_or_create_user(db: AsyncSession, telegram_id: int, user_data: dict):
    """
    Перевіряє, чи існує користувач у базі. Якщо ні — створює.
    """
    async with db.begin():
        query = select(User).where(User.telegram_id == telegram_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            # Створюємо нового користувача
            user = User(
                telegram_id=telegram_id,
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                language_code=user_data.get("language_code")
            )
            db.add(user)
            await db.commit()
            return user, True  # True означає, що це новий користувач
        return user, False  # False означає, що користувач існує
