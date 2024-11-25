# UTC:22:00
# 2024-11-25
# handlers/navigation.py
# Author: MLBB-BOSS
# Description: Navigation menu handlers
# The era of artificial intelligence.
# handlers/main_menu.py

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import get_main_keyboard
from keyboards.navigation_menu import get_navigation_keyboard  # Переконайтесь, що цей файл існує
from keyboards.profile_menu import get_profile_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, data: dict):
    session: AsyncSession = data.get('db')
    if not session:
        logger.error("Database session not found in middleware data.")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
        return
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
                f"Вітаю, {message.from_user.first_name}! Ви успішно зареєстровані.",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                f"З поверненням, {message.from_user.first_name}!",
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await session.rollback()
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: Message, data: dict):
    session: AsyncSession = data.get('db')
    if not session:
        logger.error("Database session not found in middleware data.")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
        return
    logger.info(f"User {message.from_user.id} selected 'Навігація'")
    await message.answer(
        "Меню навігації:\nОберіть потрібний розділ:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🪪 Профіль")
async def profile_menu(message: Message, data: dict):
    session: AsyncSession = data.get('db')
    if not session:
        logger.error("Database session not found in middleware data.")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
        return
    logger.info(f"User {message.from_user.id} selected 'Профіль'")
    await message.answer(
        "Ваш профіль:\nОберіть потрібний розділ:",
        reply_markup=get_profile_keyboard()
    )

@router.message(F.text == "🔙 Назад")
async def return_to_main(message: Message, data: dict):
    session: AsyncSession = data.get('db')
    if not session:
        logger.error("Database session not found in middleware data.")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
        return
    logger.info(f"User {message.from_user.id} returned to main menu")
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )
