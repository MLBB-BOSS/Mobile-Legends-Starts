from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message, session: AsyncSession) -> None:
    try:
        # Шукаємо користувача за telegram_id
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Створюємо нового користувача
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            session.add(user)
            await session.commit()
            
            await message.answer(
                f"Вітаю, {message.from_user.first_name}! Ви успішно зареєстровані."
            )
        else:
            await message.answer(
                f"З поверненням, {message.from_user.first_name}!"
            )
    except Exception as e:
        print(f"Error in start handler: {e}")
        await session.rollback()
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")
