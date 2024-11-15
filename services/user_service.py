from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.user_repository import UserRepository
from services.exceptions import UserNotFoundError, ValidationError

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)

    async def register_user(self, 
        telegram_id: int, 
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ):
        """Реєстрація нового користувача"""
        if not telegram_id:
            raise ValidationError("Telegram ID не може бути порожнім")

        # Перевіряємо чи користувач вже існує
        existing_user = await self.user_repository.get_by_telegram_id(telegram_id)
        if existing_user:
            return existing_user

        # Створюємо нового користувача
        return await self.user_repository.create_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

    async def get_user(self, telegram_id: int):
        """Отримання користувача за telegram_id"""
        user = await self.user_repository.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundError(telegram_id)
        return user

    async def update_user(self, 
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ):
        """Оновлення даних користувача"""
        user = await self.get_user(telegram_id)
        
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        return await self.user_repository.update_user(user)
