# UTC:22:12
# 2024-11-24
# handlers/navigation.py
# Author: MLBB-BOSS
# Description: Navigation menu handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import navigation_keyboard, main_menu_keyboard
from utils import get_localized_text

router = Router()

@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    await message.answer(
        get_localized_text("navigation_menu"),
        reply_markup=navigation_keyboard()
    )

@router.message(F.text == "🛡️ Персонажі")
async def show_heroes(message: Message):
    await message.answer(
        get_localized_text("heroes_menu")
    )

@router.message(F.text == "📚 Гайди")
async def show_guides(message: Message):
    await message.answer(
        get_localized_text("guides_menu")
    )

@router.message(F.text == "⚖️ Контр-піки")
async def show_counterpicks(message: Message):
    await message.answer(
        get_localized_text("counterpicks_menu")
    )

@router.message(F.text == "⚜️ Білди")
async def show_builds(message: Message):
    await message.answer(
        get_localized_text("builds_menu")
    )

@router.message(F.text == "📊 Голосування")
async def show_votes(message: Message):
    await message.answer(
        get_localized_text("votes_menu")
    )

@router.message(F.text == "🔙 Назад до Головного")
async def back_to_main_menu(message: Message):
    await message.answer(
        get_localized_text("back_to_main"),
        reply_markup=main_menu_keyboard()
    )

@router.message()
async def unknown_command(message: Message):
    await message.answer(
        get_localized_text("unknown_command")
    )
