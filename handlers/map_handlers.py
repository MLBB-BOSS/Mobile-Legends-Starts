# handlers/map_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🏞️ Огляд Мап")
async def handle_map_overview(message: Message):
    logger.info("Натиснуто кнопку '🏞️ Огляд Мап'")
    await message.answer("Дізнайтеся деталі про наявні ігрові карти.")

@router.message(F.text == "📍 Тактики на Картах")
async def handle_map_tactics(message: Message):
    logger.info("Натиснуто кнопку '📍 Тактики на Картах'")
    await message.answer("Рекомендації по тактичному розташуванню на картах.")

@router.message(F.text == "🕹️ Практика на Мапі")
async def handle_map_practice(message: Message):
    logger.info("Натиснуто кнопку '🕹️ Практика на Мапі'")
    await message.answer("Посібник для тренування стратегій на картах.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_map(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у інтерактивній карті")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)
