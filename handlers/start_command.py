from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    """Обробник команди /start"""
    await message.answer(
        "Ласкаво просимо до бота! Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )
