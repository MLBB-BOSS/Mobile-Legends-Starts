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
from utils import get_localized_text
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    logger.info(f"User {message.from_user.id} opened navigation menu")
    await message.answer(
        get_localized_text("navigation_menu"),
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🛡️ Персонажі")
async def show_heroes(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Персонажі'")
    await message.answer(
        get_localized_text("heroes_menu")
    )

@router.message(F.text == "📚 Гайди")
async def show_guides(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Гайди'")
    await message.answer(
        get_localized_text("guides_menu")
    )

@router.message(F.text == "⚖️ Контр-піки")
async def show_counterpicks(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Контр-піки'")
    await message.answer(
        get_localized_text("counterpicks_menu")
    )

@router.message(F.text == "⚜️ Білди")
async def show_builds(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Білди'")
    await message.answer(
        get_localized_text("builds_menu")
    )

@router.message(F.text == "📊 Голосування")
async def show_votes(message: Message):
    logger.info(f"User {message.from_user.id} selected 'Голосування'")
    await message.answer(
        get_localized_text("votes_menu")
    )

@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message):
    logger.info(f"User {message.from_user.id} returned to main menu from navigation")
    await message.answer(
        get_localized_text("back_to_main"),
        reply_markup=get_main_keyboard()
    )

@router.message()
async def unknown_command(message: Message):
    logger.info(f"User {message.from_user.id} sent unknown command: {message.text}")
    await message.answer(
        get_localized_text("unknown_command")
    )
