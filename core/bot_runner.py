# core/bot_runner.py

from handlers import register_routers

async def main():
    bot = Bot(
        token=API_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    register_routers(dp)  # Реєструємо всі роутери через функцію

    dp.startup.register(on_startup)

    logger.info("Запуск полінгу...")
    await dp.start_polling(bot)
