# handlers/statistics_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📊 Загальна Активність")
async def handle_general_activity(message: Message):
    logger.info("Натиснуто кнопку '📊 Загальна Активність'")
    await message.answer("Перегляньте загальні показники: кількість ігор, час у грі.")

@router.message(F.text == "🥇 Рейтинг")
async def handle_rating(message: Message):
    logger.info("Натиснуто кнопку '🥇 Рейтинг'")
    await message.answer("Ваше місце у рейтингу серед інших гравців.")

@router.message(F.text == "🎮 Ігрова Статистика")
async def handle_game_statistics(message: Message):
    logger.info("Натиснуто кнопку '🎮 Ігрова Статистика'")
    await message.answer("Детальна статистика по героях, перемогах і поразках.")

@router.message(F.text == "🔄 Назад до Профілю")
async def handle_back_to_profile_from_statistics(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Профілю' у статистиці")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
