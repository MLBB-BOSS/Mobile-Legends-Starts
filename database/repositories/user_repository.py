from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from services.database import User
from services.exceptions import DatabaseError

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Отримати користувача за telegram_id"""
        try:
            result = await self.session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseError(f"Помилка при отриманні користувача: {e}")

    async def create_user(self, 
        telegram_id: int, 
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """Створити нового користувача"""
        try:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise DatabaseError(f"Помилка при створенні користувача: {e}")

    async def update_user(self, user: User) -> User:
        """Оновити дані користувача"""
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise DatabaseError(f"Помилка при оновленні користувача: {e}")

    async def get_all_users(self) -> List[User]:
        """Отримати всіх користувачів"""
        try:
            result = await self.session.execute(select(User))
            return list(result.scalars().all())
        except Exception as e:
            raise DatabaseError(f"Помилка при отриманні всіх користувачів: {e}")

    async def delete_user(self, telegram_id: int) -> bool:
        """Видалити користувача"""
        try:
            result = await self.session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            if user:
                await self.session.delete(user)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            raise DatabaseError(f"Помилка при видаленні користувача: {e}")
