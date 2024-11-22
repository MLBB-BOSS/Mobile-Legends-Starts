# handlers/help_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📄 Інструкції")
async def handle_help_instructions(message: Message):
    logger.info("Натиснуто кнопку '📄 Інструкції'")
    await message.answer(
        "Інструкції щодо використання бота:\n"
        "1. Натисніть кнопку '🧭 Навігація' для доступу до розділів навігації.\n"
        "2. Натисніть кнопку '🪪 Мій профіль' для доступу до вашого профілю.\n"
        "3. Використовуйте підменю для більш детальної інформації та налаштувань."
    )

@router.message(F.text == "❔ FAQ")
async def handle_help_faq(message: Message):
    logger.info("Натиснуто кнопку '❔ FAQ'")
    await message.answer(
        "Часті питання:\n"
        "1. Як зареєструватися?\n"
        "2. Як змінити мову інтерфейсу?\n"
        "3. Як зв'язатися зі службою підтримки?\n"
        "…"
    )

@router.message(F.text == "📞 Підтримка")
async def handle_help_support(message: Message):
    logger.info("Натиснуто кнопку '📞 Підтримка'")
    await message.answer(
        "Контактна інформація:\n"
        "Email: support@example.com\n"
        "Телефон: +1234567890\n"
        "Telegram: @your_support_handle"
    )

@router.message(F.text == "🔄 Назад до Профілю")
async def handle_back_to_profile_from_help(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Профілю' у допомозі")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
