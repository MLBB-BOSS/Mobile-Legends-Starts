# UTC:22:00
# 2024-11-25
# handlers/navigation.py
# Author: MLBB-BOSS
# Description: Navigation menu handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import get_navigation_keyboard
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Навігація'")
    await message.answer(
        "Меню навігації:\nОберіть потрібний розділ:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🔙 Назад")
async def back_to_main_from_navigation(message: Message):
    logger.info(f"User {message.from_user.id} returned to main menu from navigation")
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )

# Додаткові обробники для навігаційних кнопок

@router.message(F.text == "🛡️ Персонажі")
async def show_heroes(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Персонажі'")
    await message.answer(
        "Перелік персонажів:",
        # Тут можна додати відповідну клавіатуру або інформацію
    )

@router.message(F.text == "📚 Гайди")
async def show_guides(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Гайди'")
    await message.answer(
        "Список гайдів:",
        # Тут можна додати відповідну клавіатуру або інформацію
    )

@router.message(F.text == "⚖️ Контр-піки")
async def show_counterpicks(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Контр-піки'")
    await message.answer(
        "Контрпіки до персонажів:",
        # Тут можна додати відповідну клавіатуру або інформацію
    )

@router.message(F.text == "⚜️ Білди")
async def show_builds(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Білди'")
    await message.answer(
        "Найкращі білди:",
        # Тут можна додати відповідну клавіатуру або інформацію
    )

@router.message(F.text == "📊 Голосування")
async def show_votes(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Голосування'")
    await message.answer(
        "Поточні голосування:",
        # Тут можна додати відповідну клавіатуру або інформацію
    )

@router.message()
async def unknown_command(message: Message):
    logger.info(f"User {message.from_user.id} sent unknown command: {message.text}")
    await message.answer(
        "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки на клавіатурі."
    )
