# handlers/voting_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📍 Поточні Опитування")
async def handle_current_polls(message: Message):
    logger.info("Натиснуто кнопку '📍 Поточні Опитування'")
    await message.answer("Приєднайтеся до активних голосувань.")

@router.message(F.text == "📋 Мої Голосування")
async def handle_my_polls(message: Message):
    logger.info("Натиснуто кнопку '📋 Мої Голосування'")
    await message.answer("Перегляньте результати та ваші участі.")

@router.message(F.text == "➕ Запропонувати Тему")
async def handle_propose_topic(message: Message):
    logger.info("Натиснуто кнопку '➕ Запропонувати Тему'")
    await message.answer("Додайте ідею для нового опитування.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_voting(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у голосуванні")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)
