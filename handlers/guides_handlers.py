# handlers/guides_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🆕 Нові Гайди")
async def handle_new_guides(message: Message):
    logger.info("Натиснуто кнопку '🆕 Нові Гайди'")
    await message.answer("Останні оновлення від команди експертів.")

@router.message(F.text == "🌟 Популярні Гайди")
async def handle_popular_guides(message: Message):
    logger.info("Натиснуто кнопку '🌟 Популярні Гайди'")
    await message.answer("Найкращі гайди, обрані гравцями.")

@router.message(F.text == "📘 Для Початківців")
async def handle_beginner_guides(message: Message):
    logger.info("Натиснуто кнопку '📘 Для Початківців'")
    await message.answer("Інструкції для новачків.")

@router.message(F.text == "🧙 Просунуті Техніки")
async def handle_advanced_techniques(message: Message):
    logger.info("Натиснуто кнопку '🧙 Просунуті Техніки'")
    await message.answer("Складні стратегії для досвідчених гравців.")

@router.message(F.text == "🛡️ Командні Стратегії")
async def handle_team_strategies(message: Message):
    logger.info("Натиснуто кнопку '🛡️ Командні Стратегії'")
    await message.answer("Тактики для командної гри.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_guides(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у гайдів")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)
