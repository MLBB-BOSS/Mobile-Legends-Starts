# handlers/navigation.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import get_navigation_menu

navigation_router = Router()

@navigation_router.message(F.text == "🛡️ Персонажі")
async def show_hero_classes(message: Message):
    """
    Відображає класи персонажів.
    """
    await message.answer("Оберіть клас героя:", reply_markup=get_hero_class_menu())

@navigation_router.message(F.text == "🔄 Повернутися до Головного Меню")
async def back_to_main_menu(message: Message):
    """
    Повертає до головного меню.
    """
    from keyboards.main_menu import get_main_menu
    await message.answer("Повертаємося до головного меню:", reply_markup=get_main_menu())
