# command: handlers/navigation_handlers.py

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Text  # Оновлений імпорт для вашої версії
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Text("🧭 Навігація"))
async def show_navigation_menu(message: Message):
    logger.info("Натиснуто кнопку '🧭 Навігація'")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Оберіть розділ навігації:", reply_markup=keyboard)

@router.message(Text("🔄 Назад"))
async def handle_back_to_main_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню навігації")
    from keyboards.menus import MainMenu
    keyboard = MainMenu.get_main_menu()
    await message.answer("Повернення до головного меню. Оберіть дію:", reply_markup=keyboard)

@router.message(Text("Місця"))
async def show_places_sub_menu(message: Message):
    logger.info("Натиснуто кнопку 'Місця'")
    from keyboards.menus import SubMenu
    keyboard = SubMenu.get_sub_menu()
    await message.answer("Ви обрали 'Місця'. Оберіть дію:", reply_markup=keyboard)

@router.message(Text("Події"))
async def show_events_sub_menu(message: Message):
    logger.info("Натиснуто кнопку 'Події'")
    from keyboards.menus import SubMenu
    keyboard = SubMenu.get_sub_menu()
    await message.answer("Ви обрали 'Події'. Оберіть дію:", reply_markup=keyboard)
