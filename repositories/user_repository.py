from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Отримати користувача за telegram_id"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create_user(
        self,
        telegram_id: int,
        nickname: str,
        email: str,
        game_id: str
    ) -> User:
        """Створити нового користувача"""
        user = User(
            telegram_id=telegram_id,
            nickname=nickname,
            email=email,
            game_id=game_id,
            is_registered=True
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        """Оновити дані користувача"""
        await self.session.commit()
        await self.session.refresh(user)
        return user
