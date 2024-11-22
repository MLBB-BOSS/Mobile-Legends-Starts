from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🪪 Мій профіль")
async def show_profile_menu(message: Message):
    logger.info("Натиснуто кнопку '🪪 Мій профіль'")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Ваш профіль. Оберіть дію:", reply_markup=keyboard)

@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message):
    logger.info("Натиснуто кнопку '📊 Статистика'")
    await message.answer("Ваша статистика: ... (дані тут)")

@router.message(F.text == "⚙️ Налаштування")
async def show_settings(message: Message):
    logger.info("Натиснуто кнопку '⚙️ Налаштування'")
    await message.answer("Налаштування вашого профілю: ... (дані тут)")

@router.message(F.text == "🔄 Назад")
async def handle_back_to_main_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню профілю")
    from keyboards.menus import MainMenu
    keyboard = MainMenu.get_main_menu()
    await message.answer("Повернення до головного меню. Оберіть дію:", reply_markup=keyboard)
