# handlers/statistics_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message):
    logger.info("Натиснуто кнопку '📊 Статистика'")
    from keyboards.statistics_menu import StatisticsMenu
    keyboard = StatisticsMenu.get_statistics_menu()
    await message.answer("Виберіть тип статистики:", reply_markup=keyboard)

@router.message(F.text == "📊 Загальна Активність")
async def handle_general_activity(message: Message):
    logger.info("Натиснуто кнопку '📊 Загальна Активність'")
    await message.answer("Ваша загальна активність: ... (дані тут)", reply_markup=None)

@router.message(F.text == "🥇 Рейтинг")
async def handle_rating(message: Message):
    logger.info("Натиснуто кнопку '🥇 Рейтинг'")
    await message.answer("Ваш рейтинг: ... (дані тут)", reply_markup=None)

@router.message(F.text == "🎮 Ігрова Статистика")
async def handle_game_statistics(message: Message):
    logger.info("Натиснуто кнопку '🎮 Ігрова Статистика'")
    await message.answer("Ваша ігрова статистика: ... (дані тут)", reply_markup=None)

@router.message(F.text == "🔄 Назад")
async def handle_back_to_profile_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню статистики")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
