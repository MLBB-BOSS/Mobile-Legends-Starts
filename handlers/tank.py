from aiogram import Router, F
from aiogram.types import Message
from keyboards.level4.tank_menu import get_tank_menu

router = Router()

@router.message(F.text == "🛡️ Танк")
async def tank_menu_handler(message: Message):
    """Обробник для класу Танк"""
    await message.answer(
        "🛡️ Танк: Оберіть героя:",
        reply_markup=get_tank_menu()
    )
