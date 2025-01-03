# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from utils.db import init_db, check_connection, AsyncSessionLocal
from utils.models import User, UserStats, BugReport, Feedback
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_profile_menu,
    get_statistics_menu,
    MenuButton
)
from dotenv import load_dotenv
from sqlalchemy.future import select
import logging

# Імпортуємо текстові константи
from texts import (
    WELCOME_NEW_USER_TEXT,
    MAIN_MENU_TEXT,
    MAIN_MENU_ERROR_TEXT,
    UNKNOWN_COMMAND_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT,
    # Додайте інші константи за потребою
)

# Імпортуємо FSM стани
from states import MenuStates

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

# Визначте обробники

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} виконав команду /start або /help")
    welcome_text = WELCOME_NEW_USER_TEXT.format(user_first_name=message.from_user.first_name)
    await message.reply(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MenuStates.MAIN_MENU)

@dp.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def main_menu_navigation(message: types.Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} перейшов до меню Навігації")
    await message.reply(
        MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name),
        reply_markup=get_navigation_menu(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MenuStates.NAVIGATION_MENU)

@dp.message_handler()
async def handle_unknown_commands(message: types.Message):
    await message.reply(
        UNKNOWN_COMMAND_TEXT,
        parse_mode=ParseMode.HTML
    )

# Додайте інші обробники, використовуючи стани з MenuStates

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
