from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import get_session

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message, session: AsyncSession) -> None:
    # Перевіряємо, чи існує користувач
    user = await session.get(User, message.from_user.id)
    
    if not user:
        # Створюємо нового користувача
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        session.add(user)
        await session.commit()
        
        await message.answer(f"Вітаю, {message.from_user.first_name}! Ви успішно зареєстровані.")
    else:
        await message.answer(f"З поверненням, {message.from_user.first_name}!")
