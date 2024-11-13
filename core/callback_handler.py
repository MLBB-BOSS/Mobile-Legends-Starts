# core/callback_handler.py

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from core.bot import dp

# Приклад обробника колбеків
@dp.callback_query_handler(Text(startswith="example"))
async def handle_example_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Це приклад обробника колбеків.")
