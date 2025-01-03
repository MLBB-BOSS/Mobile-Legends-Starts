# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F  # Імпортуємо F для фільтрації
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ParseMode
from utils.db import init_db, check_connection, AsyncSessionLocal
from utils.models import User, UserStats, BugReport, Feedback  # Імпортуємо ваші моделі
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_profile_menu,
    MenuButton
)
from dotenv import load_dotenv
from sqlalchemy.future import select
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    STATISTICS_MENU = State()
    # Додайте інші стани за необхідністю

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} виконав команду /start або /help")
    await message.reply("Привіт! Я ваш бот.", reply_markup=get_main_menu())
    await state.set_state(MenuStates.MAIN_MENU)

@dp.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def main_menu_navigation(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} перейшов до меню Навігації")
    await message.reply("Ви в меню Навігації.", reply_markup=get_navigation_menu())
    await state.set_state(MenuStates.NAVIGATION_MENU)

@dp.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def navigation_menu_heroes(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} перейшов до меню Персонажів")
    await message.reply("Ви в меню Персонажів.", reply_markup=get_heroes_menu())
    await state.set_state(MenuStates.HEROES_MENU)

@dp.message(MenuStates.HEROES_MENU, F.text == MenuButton.TANK.value)
async def handle_tank_class(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} вибрав клас Танк")
    # Ваш код для обробки вибору класу Танк
    await message.reply("Ви вибрали клас Танк.", reply_markup=get_heroes_menu())

@dp.message(MenuStates.PROFILE_MENU, F.text == MenuButton.STATISTICS.value)
async def handle_statistics_menu(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} перейшов до меню Статистики")
    await message.reply("Ви в меню Статистики.", reply_markup=get_statistics_menu())
    await state.set_state(MenuStates.STATISTICS_MENU)

# Додайте інші обробники для різних меню та станів

async def main():
    await init_db()
    if await check_connection():
        logger.info("Підключено до бази даних. Запуск бота.")
        # Запустіть диспетчер
        await dp.start_polling(bot)
    else:
        logger.error("Не вдалося підключитися до бази даних.")

if __name__ == '__main__':
    asyncio.run(main())