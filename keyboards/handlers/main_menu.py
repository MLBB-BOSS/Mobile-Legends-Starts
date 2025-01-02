from aiogram import Router
from aiogram.types import Message
from keyboards.menus import get_main_menu_keyboard

router = Router()

@router.message(lambda message: message.text == "🧭 Навігація")
async def navigation_menu(message: Message):
    """
    Обробник для переходу до навігаційного меню.
    """
    await message.answer("🧭 Це розділ навігації. Що вас цікавить?", reply_markup=get_main_menu_keyboard())

@router.message(lambda message: message.text == "🪪 Профіль")
async def profile_menu(message: Message):
    """
    Обробник для переходу до профілю.
    """
    await message.answer("🪪 Це ваш профіль. Оберіть дію.", reply_markup=get_main_menu_keyboard())
