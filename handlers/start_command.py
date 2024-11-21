from aiogram import Router, types
from aiogram.filters import Command
from utils.localization import loc
from keyboards.main_menu import MainMenu
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create router instance
router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    """
    Handler for the /start command.

    Sends a welcome message and displays the main menu keyboard.
    """
    try:
        # Send welcome message with the main menu keyboard
        await message.answer(
            loc.get_message("messages.welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
        # Log user interaction
        logger.info(f"Користувач {message.from_user.id} почав роботу з ботом.")
    except Exception as e:
        # Log any exceptions that occur
        logger.exception(f"Помилка в хендлері команди /start: {e}")
        # Send a general error message to the user
        await message.answer(
            loc.get_message("messages.errors.general")
        )
