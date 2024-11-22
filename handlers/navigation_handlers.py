# handlers/navigation_handlers.py
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(lambda message: message.text == "🔄 Назад")
async def handle_back_to_main_menu(message: Message):
    from keyboards.menus import NavigationMenu  # Імпорт з одного файлу
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=NavigationMenu.get_main_menu()
    )
