# handlers/start_handler.py

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def start_command(message: types.Message):
    """Обробник для команди /start"""
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_keyboard.add(KeyboardButton("Герої"), KeyboardButton("Інші функції"))
    await message.answer("Вітаю! Я ваш бот, готовий допомогти.", reply_markup=start_keyboard)

async def hero_list(message: types.Message):
    """Обробник для кнопки 'Герої'"""
    hero_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    hero_keyboard.add(KeyboardButton("Список класів"), KeyboardButton("Назад"))
    await message.answer("Оберіть клас героя:", reply_markup=hero_keyboard)

async def back_to_main(message: types.Message):
    """Обробник для кнопки 'Назад'"""
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    main_keyboard.add(KeyboardButton("Герої"), KeyboardButton("Інші функції"))
    await message.answer("Оберіть опцію:", reply_markup=main_keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(hero_list, lambda message: message.text == "Герої")
    dp.register_message_handler(back_to_main, lambda message: message.text == "Назад")
