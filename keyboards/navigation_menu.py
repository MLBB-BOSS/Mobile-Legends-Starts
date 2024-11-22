# handlers/navigation_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu

router = Router()

@router.message(F.text == "🔄 Назад")
async def handle_back_to_main_menu(message: Message):
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=NavigationMenu.get_main_menu()
    )
