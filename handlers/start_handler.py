from aiogram import Router
from aiogram.types import Message

start_router = Router()

@start_router.message(commands=["start"])
async def start_command(message: Message):
    await message.answer(
        "Привіт! Я готовий допомогти тобі у світі Mobile Legends. "
        "Оберіть дію через меню, або введіть запит вручну."
    )
