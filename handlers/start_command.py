from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenuKeyboard

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    """Обробник для команди /start"""
    await message.answer(
        text="Ласкаво просимо до бота! Оберіть дію:",
        reply_markup=MainMenuKeyboard.get_keyboard()
    )
