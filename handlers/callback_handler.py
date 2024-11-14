# handlers/callback_handler.py

from aiogram import Router
from aiogram.types import CallbackQuery

callback_router = Router()

@callback_router.callback_query()
async def handle_callback(call: CallbackQuery):
    await call.answer("Це тестове повідомлення для callback!")
