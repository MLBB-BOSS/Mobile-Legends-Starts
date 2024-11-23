# handlerson_ha/navigatindlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    logger.info("Натиснуто кнопку '🧭 Навігація'")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Оберіть розділ навігації:", reply_markup=keyboard)

@router.message(F.text == "Місця")
async def show_places_sub_menu(message: Message):
    logger.info("Натиснуто кнопку 'Місця'")
    from keyboards.navigation_menu import NavigationMenu  # Переконайтеся, що ім'я файла правильне
    from keyboards.menus import SubMenu  # Або відповідне меню
    keyboard = SubMenu.get_sub_menu()
    await message.answer("Ви обрали 'Місця'. Оберіть дію:", reply_markup=keyboard)

@router.message(F.text == "Події")
async def show_events_sub_menu(message: Message):
    logger.info("Натиснуто кнопку 'Події'")
    from keyboards.menus import SubMenu
    keyboard = SubMenu.get_sub_menu()
    await message.answer("Ви обрали 'Події'. Оберіть дію:", reply_markup=keyboard)

@router.message(F.text == "Персонажі")
async def show_characters_menu(message: Message):
    logger.info("Натиснуто кнопку 'Персонажі'")
    from keyboards.characters_menu import CharactersMenu
    keyboard = CharactersMenu.get_characters_menu()
    await message.answer("Ви обрали 'Персонажі'. Оберіть клас:", reply_markup=keyboard)

@router.message(F.text == "Гайди")
async def show_guides_menu(message: Message):
    logger.info("Натиснуто кнопку 'Гайди'")
    # Створіть та використовуйте відповідне меню
    await message.answer("Ви обрали 'Гайди'. Оберіть дію:", reply_markup=None)  # Замініть reply_markup при необхідності

@router.message(F.text == "🔄 Назад")
async def handle_back_to_main_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню навігації")
    from keyboards.menus import MainMenu
    keyboard = MainMenu.get_main_menu()
    await message.answer("Повернення до головного меню. Оберіть дію:", reply_markup=keyboard)
