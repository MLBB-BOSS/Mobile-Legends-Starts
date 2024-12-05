# handlers_navigation.py

from aiogram import types
from aiogram.dispatcher import Dispatcher

from keyboards.menus import MenuButton

async def show_meta_menu(message: types.Message):
    await message.answer("📈 <b>Мета:</b> Тут ви знайдете актуальну інформацію про мету гри.", parse_mode='HTML')

async def show_m6_menu(message: types.Message):
    await message.answer("🎮 <b>М6:</b> Останні новини та події про турніри M6.", parse_mode='HTML')

async def show_gpt_menu(message: types.Message):
    await message.answer("👾 <b>GPT:</b> Інтерактивна допомога на базі GPT для будь-яких запитань та порад.", parse_mode='HTML')

def register_navigation_handlers(dp: Dispatcher):
    dp.register_message_handler(show_meta_menu, text=MenuButton.META.value)
    dp.register_message_handler(show_m6_menu, text=MenuButton.M6.value)
    dp.register_message_handler(show_gpt_menu, text=MenuButton.GPT.value)
