from aiogram import Router, F
from aiogram.types import Message
from keyboards.level3.counter_picks_menu import get_counter_picks_menu

router = Router()

@router.message(F.text == "⚖️ Контр-піки")
async def counter_picks_menu_handler(message: Message):
    """Обробник для меню Контр-піків"""
    await message.answer(
        "⚖️ Контр-піки: Оберіть опцію для продовження.",
        reply_markup=get_counter_picks_menu()
    )
