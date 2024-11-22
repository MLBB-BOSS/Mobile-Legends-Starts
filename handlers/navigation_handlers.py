# handlers/navigation_handlers.py

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from keyboards.navigation_menu import get_navigation_menu
from keyboards.hero_menu import get_hero_class_menu

navigation_router = Router()

@navigation_router.message(Text("Персонажі"))
async def show_hero_classes_menu(message: Message):
    await message.answer("Оберіть клас героя:", reply_markup=get_hero_class_menu())

@navigation_router.message(Text(["Гайди", "Контрпіки"]))
async def show_placeholder(message: Message):
    await message.answer(f"Функція '{message.text}' ще на стадії розробки.")

@navigation_router.message(Text("🔄 Назад"))
async def navigation_back_to_main(message: Message):
    from keyboards.menus import get_main_menu
    await message.answer("Повернення до головного меню:", reply_markup=get_main_menu())
