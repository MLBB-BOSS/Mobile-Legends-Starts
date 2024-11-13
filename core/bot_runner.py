# core/bot_runner.py

import logging
from aiogram import executor
from core.bot import dp, on_startup, on_shutdown

logger = logging.getLogger(__name__)

async def run_bot(session_factory):
    """
    Функція для запуску бота.
    
    Args:
        session_factory: Фабрика для створення сесій бази даних.
    """
    try:
        await dp.start_polling(
            on_startup=lambda dp: on_startup(dp, session_factory),
            on_shutdown=on_shutdown,
            skip_updates=True
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise
