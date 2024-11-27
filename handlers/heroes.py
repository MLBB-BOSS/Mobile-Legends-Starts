from aiogram import Router, F
from aiogram.types import Message
from keyboards.level3.heroes_menu import get_heroes_menu

router = Router()

@router.message(F.text == "🛡️ Персонажі")
async def heroes_menu_handler(message: Message):
    """Обробник для переходу до меню персонажів"""
    await message.answer(
        "🛡️ Персонажі: Оберіть клас персонажів:",
        reply_markup=get_heroes_menu()
    )
