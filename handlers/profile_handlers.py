# handlers/profile_handlers.py
# UTC:22:00
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers for profile menu and user-related actions
# The era of artificial intelligence.
# handlers/profile_handlers.py
# UTC:22:00
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers for profile menu and user-related actions
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import get_profile_keyboard
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "👤 Профіль")
async def show_profile(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed profile")
        await message.answer(
            "Ваш профіль:\n\n"
            "🎮 Нікнейм: Не встановлено\n"
            "🏆 Рейтинг: 0\n"
            "🎯 Досягнення: 0\n"
            "📊 Статистика: Недоступна",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in profile handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "📈 Статистика")
async def show_statistics(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed statistics")
        await message.answer(
            "📈 Ваша статистика:\n\n"
            "🎮 Ігор зіграно: 0\n"
            "✨ Середній KDA: 0/0/0\n"
            "🏆 Перемог: 0\n"
            "💔 Поразок: 0",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in statistics handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🏆 Досягнення")
async def show_achievements(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed achievements")
        await message.answer(
            "🏆 Ваші досягнення:\n\n"
            "Поки що немає досягнень.\n"
            "Грайте більше, щоб отримувати нові досягнення!",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in achievements handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "💌 Зворотний Зв'язок")
async def show_feedback(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed feedback")
        await message.answer(
            "💌 Зворотний зв'язок:\n\n"
            "Для зв'язку з адміністрацією напишіть: @admin_username",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in feedback handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "⚙️ Налаштування")
async def show_settings(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed settings")
        await message.answer(
            "⚙️ Налаштування:\n\n"
            "🎮 Нікнейм: Змінити\n"
            "🔔 Сповіщення: Увімк\n"
            "🌐 Мова: Українська",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in settings handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "❓ Допомога")
async def show_help(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed help")
        await message.answer(
            "❓ Допомога:\n\n"
            "👤 Профіль - перегляд вашого профілю\n"
            "📈 Статистика - ваша ігрова статистика\n"
            "🏆 Досягнення - ваші нагороди\n"
            "💌 Зворотний зв'язок - зв'язок з адміністрацією\n"
            "⚙️ Налаштування - змінити налаштування бота",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in help handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🔙 Назад")
async def back_to_main_from_profile(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to main menu from profile")
        await message.answer(
            "Головне меню:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in back to main menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
