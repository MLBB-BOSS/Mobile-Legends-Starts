import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.text import Text  # Виправлений імпорт
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ParseMode
from utils.db import init_db, check_connection, AsyncSessionLocal
from utils.models import User, UserStats, BugReport, Feedback  # Імпортуйте ваші моделі
from keyboards.menus import get_main_menu, get_navigation_menu, MenuButton, get_heroes_menu  # Імпортуйте потрібні клавіатури
from dotenv import load_dotenv
from sqlalchemy.future import select

# Завантажте змінні середовища з .env файлу
load_dotenv()

# Отримайте токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

# Створіть екземпляри бота та диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Визначте стани
class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    PROFILE_MENU = State()
    # Додайте інші стани за необхідністю

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Привіт! Я ваш бот.", reply_markup=get_main_menu())
    await state.set_state(MenuStates.MAIN_MENU)

@dp.message(MenuStates.MAIN_MENU, Text(equals=MenuButton.NAVIGATION.value))
async def main_menu_navigation(message: types.Message, state: FSMContext):
    await message.reply("Ви в меню Навігації.", reply_markup=get_navigation_menu())
    await state.set_state(MenuStates.NAVIGATION_MENU)

@dp.message(MenuStates.NAVIGATION_MENU, Text(equals=MenuButton.HEROES.value))
async def navigation_menu_heroes(message: types.Message, state: FSMContext):
    await message.reply("Ви в меню Персонажів.", reply_markup=get_heroes_menu())
    await state.set_state(MenuStates.HEROES_MENU)

# Додайте інші обробники для різних меню та станів

async def main():
    await init_db()
    if await check_connection():
        # Запустіть диспетчер
        await dp.start_polling(bot)
    else:
        print("Не вдалося підключитися до бази даних.")

if __name__ == '__main__':
    asyncio.run(main())
