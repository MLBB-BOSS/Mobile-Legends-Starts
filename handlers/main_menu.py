from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User
from keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession) -> None:
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
                text=f"Вітаю, {message.from_user.first_name}! Ви успішно зареєстровані.",
                reply_markup=main_menu_keyboard()
            )
        else:
            await message.answer(
                text=f"З поверненням, {message.from_user.first_name}!",
                reply_markup=main_menu_keyboard()
            )
            
    except Exception as e:
        print(f"Error in start handler: {e}")
        await session.rollback()
        await message.answer(
            text="Сталася помилка при обробці команди. Спробуйте пізніше."
        )
