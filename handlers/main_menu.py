from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text

from keyboards import main_menu_keyboard
from utils import get_localized_text
from database import async_session
from models import User

router = Router()

def register_handlers_main_menu(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Додавання користувача до бази даних
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            new_user = User(
                id=message.from_user.id,
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            session.add(new_user)
            await session.commit()
    await message.answer(
        get_localized_text("greeting"),
        reply_markup=main_menu_keyboard()
    )

@router.message(Text(equals="Мій профіль"))
async def my_profile(message: Message):
    # Отримання інформації про користувача з бази даних
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            response = f"Ваш ID: {user.telegram_id}\nВаш username: @{user.username}"
        else:
            response = "Користувача не знайдено."
    await message.answer(response)

@router.message(Text(equals="Навігація"))
async def navigation(message: Message):
    from keyboards import navigation_menu_keyboard
    await message.answer(
        get_localized_text("navigation_prompt"),
        reply_markup=navigation_menu_keyboard()
    )

@router.message()
async def unknown_message(message: Message):
    await message.answer(get_localized_text("unknown_command"))
