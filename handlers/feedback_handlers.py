# handlers/feedback_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "✏️ Надіслати Відгук")
async def handle_send_feedback(message: Message):
    logger.info("Натиснуто кнопку '✏️ Надіслати Відгук'")
    await message.answer("Поділіться своїми ідеями або пропозиціями.")

@router.message(F.text == "🐛 Повідомити про Помилку")
async def handle_report_bug(message: Message):
    logger.info("Натиснуто кнопку '🐛 Повідомити про Помилку'")
    await message.answer("Залиште інформацію про знайдену проблему.")

@router.message(F.text == "🔄 Назад до Профілю")
async def handle_back_to_profile_from_feedback(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Профілю' у зворотному зв'язку")
    from keyboards.menus import ProfileMenu
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Повернення до профілю. Оберіть дію:", reply_markup=keyboard)
