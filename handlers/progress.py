# handlers/progress.py
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from utils import generate_rating_chart

router = Router()

@router.message(Command("my_progress"))
async def show_progress(message: Message):
    # Ваш хендлер
    ...
