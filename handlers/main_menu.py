from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import (
    get_main_keyboard, get_navigation_keyboard, get_profile_keyboard,
    get_guides_keyboard, get_counterpicks_keyboard, get_builds_keyboard
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, db: AsyncSession):
    try:
        result = await db.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
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
    try:
        logger.info(f"User {message.from_user.id} selected 'Навігація'")
        await message.answer(
            "Меню навігації:\nОберіть потрібний розділ:",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in navigation menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "🪪 Профіль")
async def profile_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Профіль'")
        await message.answer(
            "Ваш профіль:\nОберіть потрібний розділ:",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in profile menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "🔙 Назад")
async def return_to_main(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to main menu")
        await message.answer(
            "Головне меню:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in return to main menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "📚 Гайди")
async def guides_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Гайди'")
        await message.answer(
            "Меню гайдів:\нОберіть потрібний розділ:",
            reply_markup=get_guides_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in guides menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "⚔️ Контрпіки")
async def counterpicks_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Контрпіки'")
        await message.answer(
            "Меню контрпіків:\нОберіть потрібний розділ:",
            reply_markup=get_counterpicks_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in counterpicks menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "🔧 Білди")
async def builds_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Білди'")
        await message.answer(
            "Меню білдів:\нОберіть потрібний розділ:",
            reply_markup=get_builds_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in builds menu handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")

@router.message(F.text == "◀️ Назад до Навігації")
async def back_to_navigation(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to navigation menu")
        await message.answer(
            "Меню навігації:\нОберіть потрібний розділ:",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in back to navigation handler: {e}")
        await message.answer("Сталася помилка при обробці команди. Спробуйте пізніше.")
