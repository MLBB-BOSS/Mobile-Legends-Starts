from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.states import RegistrationStates
from services.reply_keyboard import get_main_keyboard
from services.database import async_session, User
from sqlalchemy import select
import re

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    async with async_session() as session:
        # Перевіряємо чи користувач вже зареєстрований
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user and user.is_registered:
            await message.answer(
                f"З поверненням, {user.nickname}! 👋\nОберіть опцію з меню:",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "Ласкаво просимо! Давайте розпочнемо реєстрацію.\n"
                "Введіть ваш нікнейм (мінімум 3 символи):"
            )
            await state.set_state(RegistrationStates.waiting_for_nickname)

@router.message(RegistrationStates.waiting_for_nickname)
async def process_nickname(message: Message, state: FSMContext):
    nickname = message.text.strip()
    
    if len(nickname) < 3:
        await message.answer("Нікнейм повинен містити мінімум 3 символи. Спробуйте ще раз:")
        return
    
    await state.update_data(nickname=nickname)
    await message.answer("Чудово! Тепер введіть вашу електронну пошту:")
    await state.set_state(RegistrationStates.waiting_for_email)

@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip().lower()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        await message.answer("Некоректний формат email. Спробуйте ще раз:")
        return
    
    async with async_session() as session:
        # Перевіряємо чи email вже існує
        result = await session.execute(
            select(User).where(User.email == email)
        )
        existing_email = result.scalar_one_or_none()
        
        if existing_email:
            await message.answer("Цей email вже зареєстрований. Спробуйте інший:")
            return
    
    await state.update_data(email=email)
    await message.answer("Чудово! Тепер введіть ваш ID з Mobile Legends (тільки цифри):")
    await state.set_state(RegistrationStates.waiting_for_game_id)

@router.message(RegistrationStates.waiting_for_game_id)
async def process_game_id(message: Message, state: FSMContext):
    game_id = message.text.strip()
    
    if not game_id.isdigit():
        await message.answer("ID повинен містити тільки цифри. Спробуйте ще раз:")
        return
    
    async with async_session() as session:
        # Перевіряємо чи game_id вже існує
        result = await session.execute(
            select(User).where(User.game_id == game_id)
        )
        existing_game_id = result.scalar_one_or_none()
        
        if existing_game_id:
            await message.answer("Цей ID вже зареєстрований. Спробуйте інший:")
            return
        
        user_data = await state.get_data()
        new_user = User(
            telegram_id=message.from_user.id,
            nickname=user_data['nickname'],
            email=user_data['email'],
            game_id=game_id,
            is_registered=True
        )
        
        try:
            session.add(new_user)
            await session.commit()
            await message.answer(
                f"Реєстрація завершена! Вітаємо, {user_data['nickname']}! 🎉\n"
                "Ви можете скористатися меню для подальших дій:",
                reply_markup=get_main_keyboard()
            )
        except Exception as e:
            await session.rollback()
            await message.answer("Помилка при реєстрації. Спробуйте ще раз з /start")
        finally:
            await state.clear()
