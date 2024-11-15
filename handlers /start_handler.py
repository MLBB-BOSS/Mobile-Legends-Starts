from aiogram import Router, types
from aiogram.filters import Command

router = Router(name="start_router")

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Вітаю! Я бот MLS. Чим можу допомогти?")
