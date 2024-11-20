# core/bot_runner.py

async def setup_dispatcher() -> Dispatcher:
    """Налаштування диспетчера"""
    try:
        dp = Dispatcher()
        
        # Налаштування обробки помилок
        dp.errors.register(error_handler)
        
        return dp
    except Exception as e:
        logger.error(f"Помилка при налаштуванні диспетчера: {e}")
        raise

async def main() -> None:
    """Головна функція запуску бота"""
    try:
        # Створюємо та налаштовуємо диспетчер
        dp = await setup_dispatcher()
        
        # Налаштовуємо бота
        bot = await setup_bot()
        
        # Налаштовуємо роутери
        setup_routers(dp)
        
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise
    finally:
        if 'bot' in locals():
            await bot.session.close()
            logger.info("З'єднання з Telegram закрито")
