# File: handlers/profile_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, Text
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()
profile_menu = ProfileMenu()

@router.message(Command("profile"))
async def show_profile_menu(message: Message):
    """Handler for the /profile command"""
    try:
        await message.answer(
            text=loc.get_message("messages.profile.main_menu") or "Виберіть опцію профілю:",
            reply_markup=profile_menu.get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка показу профільного меню: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@router.message(F.text == loc.get_message("buttons.statistics") or F.text == "📊 Статистика")
async def show_statistics_menu(message: Message):
    """Handler for statistics button"""
    try:
        await message.answer(
            text=loc.get_message("messages.profile.statistics_menu") or "Оберіть тип статистики:",
            reply_markup=profile_menu.get_statistics_menu()
        )
    except Exception as e:
        logger.error(f"Помилка показу меню статистики: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@router.message(F.text == loc.get_message("buttons.achievements") or F.text == "🏆 Досягнення")
async def show_achievements_menu(message: Message):
    """Handler for achievements button"""
    try:
        await message.answer(
            text=loc.get_message("messages.profile.achievements_menu") or "Оберіть розділ досягнень:",
            reply_markup=profile_menu.get_achievements_menu()
        )
    except Exception as e:
        logger.error(f"Помилка показу меню досягнень: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@router.message(F.text == loc.get_message("buttons.personal_stats") or F.text == "👤 Особиста статистика")
async def show_personal_stats(message: Message):
    """Handler for personal statistics button"""
    try:
        # Here you would implement the logic to fetch and display personal statistics
        stats_text = "Ваша особиста статистика:\n" # Placeholder text
        await message.answer(
            text=stats_text,
            reply_markup=profile_menu.get_statistics_menu()
        )
    except Exception as e:
        logger.error(f"Помилка показу особистої статистики: {e}")
        await message.answer("Виникла помилка при завантаженні статистики.")

@router.message(F.text == loc.get_message("buttons.global_stats") or F.text == "🌐 Загальна статистика")
async def show_global_stats(message: Message):
    """Handler for global statistics button"""
    try:
        # Here you would implement the logic to fetch and display global statistics
        stats_text = "Загальна статистика турнірів:\n" # Placeholder text
        await message.answer(
            text=stats_text,
            reply_markup=profile_menu.get_statistics_menu()
        )
    except Exception as e:
        logger.error(f"Помилка показу загальної статистики: {e}")
        await message.answer("Виникла помилка при завантаженні статистики.")

@router.message(F.text == loc.get_message("buttons.back") or F.text == "↩️ Назад")
async def handle_back_button(message: Message):
    """Handler for back button"""
    try:
        await show_profile_menu(message)
    except Exception as e:
        logger.error(f"Помилка обробки кнопки назад: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")
