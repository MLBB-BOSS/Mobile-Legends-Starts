from aiogram import Router
from aiogram.types import Message
from keyboards.main_menu import MainMenuKeyboard

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    await message.answer("Ласкаво просимо до бота!", reply_markup=MainMenuKeyboard.get_keyboard())
