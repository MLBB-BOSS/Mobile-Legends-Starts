# handlers/guides_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "Гайди")
async def show_guides_menu(message: Message):
    logger.info("Натиснуто кнопку 'Гайди'")
    # Створіть відповідне меню для гайдів
    await message.answer("Виберіть гайд:", reply_markup=None)  # Замініть reply_markup при необхідності

@router.message(F.text == "🔄 Назад")
async def handle_back_to_navigation_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню гайдів")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до меню навігації. Оберіть опцію:", reply_markup=keyboard)
