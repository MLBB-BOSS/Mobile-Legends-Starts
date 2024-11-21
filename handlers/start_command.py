from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command  # Використовуємо новий фільтр
from keyboards.main_menu import MainMenuKeyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    """Обробник для команди /start"""
    await message.answer(
        text="Ласкаво просимо до бота! Оберіть дію:",
        reply_markup=MainMenuKeyboard.get_keyboard()
    )
