# core/info_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from core.bot import dp

@dp.message_handler(Command("info"))
async def send_info(message: types.Message):
    info_text = (
        "👋 <b>Ласкаво просимо до нашого бота!</b>\n"
        "Цей бот допоможе вам з інформацією про героїв та керування скріншотами."
    )
    await message.reply(info_text, parse_mode="HTML")
