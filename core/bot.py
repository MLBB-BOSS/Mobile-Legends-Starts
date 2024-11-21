# File: core/bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.main_menu import MainMenu
from keyboards.profile_menu import ProfileMenu
from keyboards.navigation_menu import NavigationMenu
from utils.localization import loc
from handlers import profile_handlers, navigation_handlers
import logging
import asyncio
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Register all handlers
dp.include_router(profile_handlers.router)
dp.include_router(navigation_handlers.router)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handler for the /start command"""
    try:
        # Create keyboard
        keyboard = MainMenu().get_main_menu()
        
        # Get user's language code (if needed for localization)
        user_language = message.from_user.language_code
        
        await message.reply(
            loc.get_message("messages.welcome"),
            reply_markup=keyboard
        )
        logger.info(f"User {message.from_user.id} started the bot (lang: {user_language})")
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        await message.reply(loc.get_message("messages.errors.general"))

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handler for the /help command"""
    try:
        help_text = loc.get_message("messages.help")
        await message.reply(help_text)
        logger.info(f"User {message.from_user.id} requested help")
    except Exception as e:
        logger.error(f"Error in help command: {e}", exc_info=True)
        await message.reply(loc.get_message("messages.errors.general"))

async def on_startup(dispatcher: Dispatcher):
    """Startup actions"""
    try:
        # Set bot commands
        await bot.set_my_commands([
            types.BotCommand(command="start", description="Запустити бота"),
            types.BotCommand(command="help", description="Отримати допомогу"),
            types.BotCommand(command="profile", description="Мій профіль"),
            types.BotCommand(command="settings", description="Налаштування")
        ])
        logger.info("Bot commands have been set")
        
        # Additional startup tasks can be added here
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)

async def on_shutdown(dispatcher: Dispatcher):
    """Shutdown actions"""
    try:
        # Close bot instance
        await bot.session.close()
        logger.info("Bot has been shut down")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)

async def main():
    """Main function to start the bot"""
    try:
        # Register startup and shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Start polling
        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Critical error in main: {e}", exc_info=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
