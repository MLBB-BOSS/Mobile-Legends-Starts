from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.states import RegistrationStates
from services.database import async_session, User
from sqlalchemy import select
import logging
import re

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        async with async_session() as session:
            # Перевіряємо чи користувач вже зареєстрований
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
            
            if user and user.is_registered:
                await message.answer(
                    f"З поверненням, {user.nickname}! 👋\n"
                    "Оберіть опцію з меню нижче:"
                )
            else:
                await message.answer(
                    "Ласкаво просимо до MLS Bot! 🎮\n"
                    "Давайте розпочнемо реєстрацію.\n"
                    "Введіть ваш нікнейм (мінімум 3 символи):"
                )
                await state.set_state(RegistrationStates.waiting_for_nickname)
    except Exception as e:
        logger.error(f"Помилка при обробці команди start: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше або зверніться до адміністратора.")

@router.message(RegistrationStates.waiting_for_nickname)
async def process_nickname(message: Message, state: FSMContext):
    nickname = message.text.strip()
    
    if len(nickname) < 3:
        await message.answer("Нікнейм повинен містити мінімум 3 символи. Спробуйте ще раз:")
        return
    
    await state.update_data(nickname=nickname)
    await message.answer(
        "Чудово! ✨\n"
        "Тепер введіть вашу електронну пошту:"
    )
    await state.set_state(RegistrationStates.waiting_for_email)

@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip().lower()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        await message.answer("Некоректний формат email. Спробуйте ще раз:")
        return
    
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            if result.scalar_one_or_none():
                await message.answer("Цей email вже зареєстрований. Використайте інший:")
                return
            
            await state.update_data(email=email)
            await message.answer(
                "Чудово! 📧\n"
                "Тепер введіть ваш ID з Mobile Legends (тільки цифри):"
            )
            await state.set_state(RegistrationStates.waiting_for_game_id)
    except Exception as e:
        logger.error(f"Помилка при обробці email: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@router.message(RegistrationStates.waiting_for_game_id)
async def process_game_id(message: Message, state: FSMContext):
    game_id = message.text.strip()
    
    if not game_id.isdigit():
        await message.answer("ID повинен містити тільки цифри. Спробуйте ще раз:")
        return
    
    try:
        async with async_session() as session:
            # Перевіряємо чи game_id вже існує
            result = await session.execute(
                select(User).where(User.game_id == game_id)
            )
            if result.scalar_one_or_none():
                await message.answer("Цей ID вже зареєстрований. Використайте інший:")
                return
            
            user_data = await state.get_data()
            new_user = User(
                telegram_id=message.from_user.id,
                nickname=user_data['nickname'],
                email=user_data['email'],
                game_id=game_id,
                is_registered=True
            )
            
            session.add(new_user)
            await session.commit()
            
            await message.answer(
                f"🎉 Вітаємо, {user_data['nickname']}!\n"
                "Реєстрація успішно завершена.\n"
                "Тепер ви можете користуватися всіма функціями бота!"
            )
            await state.clear()
    except Exception as e:
        logger.error(f"Помилка при реєстрації користувача: {e}")
        await message.answer("Виникла помилка при реєстрації. Спробуйте пізніше.")
