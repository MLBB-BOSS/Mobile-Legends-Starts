from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.states import RegistrationStates
from services.database import async_session, User
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
            
            if user and user.is_registered:
                await message.answer(
                    f"З поверненням, {user.nickname}! 👋\nОберіть опцію з меню нижче:"
                )
            else:
                await message.answer(
                    "Ласкаво просимо до MLS Bot! 🎮\nДавайте розпочнемо реєстрацію.\nВведіть ваш Game ID (8 цифр):"
                )
                await state.set_state(RegistrationStates.waiting_for_game_id)
    except Exception as e:
        logger.error(f"Помилка при обробці команди start: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше або зверніться до адміністратора.")

@router.message(RegistrationStates.waiting_for_game_id)
async def process_game_id(message: Message, state: FSMContext):
    game_id = message.text.strip()
    
    if not game_id.isdigit() or len(game_id) != 8:
        await message.answer("Game ID має містити 8 цифр. Спробуйте ще раз:")
        return
    
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.game_id == game_id)
            )
            if result.scalar_one_or_none():
                await message.answer("Цей ID вже зареєстрований. Використайте інший:")
                return

            new_user = User(
                telegram_id=message.from_user.id,
                nickname=message.from_user.username,
                game_id=game_id,
                is_registered=True
            )
            session.add(new_user)
            await session.commit()
            
            await message.answer(
                f"🎉 Вітаємо, {message.from_user.username}!\nРеєстрація успішно завершена.\nТепер ви можете користуватися всіма функціями бота!"
            )
            await state.clear()
    except Exception as e:
        logger.error(f"Помилка при реєстрації користувача: {e}")
        await message.answer("Виникла помилка при реєстрації. Спробуйте пізніше.")
