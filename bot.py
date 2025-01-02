# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers import setup_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    setup_handlers(dp)

    logger.info("Starting bot...")

    try:
        asyncio.run(dp.start_polling(bot))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")

if __name__ == "__main__":
    main()

# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

# handlers/__init__.py
from aiogram import Dispatcher
from handlers.menu_handler import router as menu_router
from handlers.intro_handler import router as intro_router

def setup_handlers(dp: Dispatcher):
    dp.include_router(menu_router)
    dp.include_router(intro_router)

# handlers/menu_handler.py
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.menu_states import MainMenuState
from keyboards.menus import get_main_menu

router = Router()

@router.message(MainMenuState.main)
async def handle_main_menu(message: Message, state: FSMContext):
    await message.answer("Welcome to the Main Menu!", reply_markup=get_main_menu())

# handlers/intro_handler.py
from aiogram import Router
from aiogram.types import Message
from states.menu_states import MainMenuState
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def intro_handler(message: Message, state: FSMContext):
    await state.set_state(MainMenuState.main)
    await message.answer("Introduction completed! Moving to main menu.")

# states/menu_states.py
from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    main = State()

# keyboards/menus.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Option 1")],
            [KeyboardButton(text="Option 2")]
        ],
        resize_keyboard=True
    )

# .env
TELEGRAM_BOT_TOKEN=your_bot_token_here
