# core/bot_runner.py

import asyncio
import logging
from aiogram import Dispatcher
from core.bot import bot, dp
from handlers.basic_handlers import basic_router
from handlers.callback_handler import callback_router
from handlers.help_handler import help_router
from handlers.heroes_info_handler import heroes_info_router
from handlers.info_handler import info_router
from handlers.leaderboard_handler import leaderboard_router
from handlers.profile_handler import profile_router
from handlers.screenshot_handler import screenshot_router

logging.basicConfig(level=logging.INFO)

async def on_startup():
    dp.include_router(basic_router)
    dp.include_router(callback_router)
    dp.include_router(help_router)
    dp.include_router(heroes_info_router)
    dp.include_router(info_router)
    dp.include_router(leaderboard_router)
    dp.include_router(profile_router)
    dp.include_router(screenshot_router)

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("👋 Бот зупинено користувачем.")
