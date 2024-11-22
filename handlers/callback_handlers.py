from aiogram import Router, F, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "example_callback")
async def example_callback_handler(callback: CallbackQuery):
    await callback.message.answer("Оброблено!")
    await callback.answer()
