from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import get_profile_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "📈 Статистика")
async def show_statistics(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed statistics")
        await message.answer(
            "📈 Ваша статистика:\n\n"
            "🎮 Ігор зіграно: 0\n"
            "✨ Середній KDA: 0/0/0\n"
            "🏆 Перемог: 0\n"
            "💔 Поразок: 0",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in statistics handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🏆 Досягнення")
async def show_achievements(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed achievements")
        await message.answer(
            "🏆 Ваші досягнення:\n\n"
            "Поки що немає досягнень.\n"
            "Грайте більше, щоб отримувати нові досягнення!",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in achievements handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "💌 Зворотний Зв'язок")
async def show_feedback(message: Message):
    try:
        logger.info(f"User {message.from_user.id} accessed feedback")
        await message.answer(
            "💌 Зворотний Зв'язок:\n\n"
            "Будь ласка, надайте ваші відгуки та пропозиції.",
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in feedback handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

# Additional handlers...
