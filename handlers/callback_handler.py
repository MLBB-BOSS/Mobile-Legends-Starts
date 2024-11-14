# handlers/callback_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher

async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer("Це відповідь на callback!")

def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(some_callback_handler, text="some_callback_data")
