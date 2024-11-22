# handlers/achievements_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🎖️ Мої Бейджі")
async def handle_my_badges(message: Message):
    logger.info("Натиснуто кнопку '🎖️ Мої Бейджі'")
    await message.answer("Отримані нагороди та відзнаки.")

@router.message(F.text == "🚀 Прогрес")
async def handle_progress(message: Message):
    logger.info("Натиснуто кнопку '🚀 Прогрес'")
    await message.answer("Відстежуйте свій прогрес до нових досягнень.")

@router.message(F.text == "🏅 Турнірна Статистика")
async def handle_tournament_statistics(message: Message):
    logger.info("Натиснуто кнопку '🏅 Турнірна Статистика'")
    await message.answer("Показники участі у турнірах.")

@router.message(F.text == "🔄 Назад до Профілю")
async def handle_back_to_profile_from_achievements(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Профілю' у досягненнях")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
