# core/bot_runner.py
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from handlers import (
    start_router,
    navigation_router,
    profile_router,
    characters_router,
    statistics_router,
    achievements_router,
    settings_router,
    feedback_router,
    help_router,
    heroes_router,
    guides_router,
    counter_picks_router,
    builds_router,
    voting_router,
    map_router,
    game_modes_router
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("Не знайдено TELEGRAM_BOT_TOKEN у змінних середовища!")

async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустити бота"),
        BotCommand(command="/help", description="Отримати довідку"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Команди бота успішно встановлені.")

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await setup_bot_commands(bot)
    logger.info("Бот успішно запущено.")

async def main():
    bot = Bot(
        token=API_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(navigation_router)
    dp.include_router(profile_router)
    dp.include_router(characters_router)
    dp.include_router(statistics_router)
    dp.include_router(achievements_router)
    dp.include_router(settings_router)
    dp.include_router(feedback_router)
    dp.include_router(help_router)
    dp.include_router(heroes_router)
    dp.include_router(guides_router)
    dp.include_router(counter_picks_router)
    dp.include_router(builds_router)
    dp.include_router(voting_router)
    dp.include_router(map_router)
    dp.include_router(game_modes_router)
    # Додайте інші роутери тут

    dp.startup.register(on_startup)

    logger.info("Запуск полінгу...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот зупинено!")
