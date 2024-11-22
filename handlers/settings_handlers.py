# handlers/settings_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🌐 Мова Інтерфейсу")
async def handle_interface_language(message: Message):
    logger.info("Натиснуто кнопку '🌐 Мова Інтерфейсу'")
    await message.answer("Змініть мову інтерфейсу (Українська, Англійська тощо).")

@router.message(F.text == "🆔 Змінити Username")
async def handle_change_username(message: Message):
    logger.info("Натиснуто кнопку '🆔 Змінити Username'")
    await message.answer("Налаштуйте своє ім'я користувача.")

@router.message(F.text == "🛡️ Оновити ID Гравця")
async def handle_update_player_id(message: Message):
    logger.info("Натиснуто кнопку '🛡️ Оновити ID Гравця'")
    await message.answer("Синхронізуйте профіль з грою.")

@router.message(F.text == "🔔 Сповіщення")
async def handle_notifications(message: Message):
    logger.info("Натиснуто кнопку '🔔 Сповіщення'")
    await message.answer("Увімкніть або вимкніть інформування.")

@router.message(F.text == "🔄 Назад до Профілю")
async def handle_back_to_profile_from_settings(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Профілю' у налаштуваннях")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
