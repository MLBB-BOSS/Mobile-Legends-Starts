# handlers/builds_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🏗️ Створити Білд")
async def handle_create_build(message: Message):
    logger.info("Натиснуто кнопку '🏗️ Створити Білд'")
    await message.answer("Зберіть власний набір предметів для гри.")

@router.message(F.text == "📄 Мої Білди")
async def handle_my_builds(message: Message):
    logger.info("Натиснуто кнопку '📄 Мої Білди'")
    await message.answer("Ваші створені білди.")

@router.message(F.text == "💎 Популярні Білди")
async def handle_popular_builds(message: Message):
    logger.info("Натиснуто кнопку '💎 Популярні Білди'")
    await message.answer("Перегляньте найуспішніші білди спільноти.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_builds(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у білдах")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)
