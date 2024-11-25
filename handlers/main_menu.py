# handlers/main_menu.py
# UTC:22:00
# 2024-11-25
# Author: MLBB-BOSS
# Description: Main menu message handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import get_main_keyboard
from keyboards.navigation_menu import get_navigation_keyboard
from keyboards.profile_menu import get_profile_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, db: AsyncSession):
    try:
        # Шукаємо користувача за telegram_id
        result = await db.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # Створюємо нового користувача
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            db.add(user)
            await db.commit()

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
        await db.rollback()
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Навігація'")
    await message.answer(
        "Меню навігації:\nОберіть потрібний розділ:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🪪 Профіль")
async def profile_menu(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Профіль'")
    await message.answer(
        "Ваш профіль:\nОберіть потрібний розділ:",
        reply_markup=get_profile_keyboard()
    )

@router.message(F.text == "🔙 Назад")
async def return_to_main(message: Message):
    logger.info(f"User {message.from_user.id} returned to main menu")
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )
