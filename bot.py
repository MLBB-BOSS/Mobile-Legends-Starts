import asyncio
import logging
import os
import aiohttp  # Додано для роботи з HTTP-запитами
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # Додано для встановлення параметрів за замовчуванням
from config import settings
from handlers.buttons import register_buttons_handlers  # Імпорт обробників кнопок
from handlers_navigation import register_navigation_handlers

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%м-%д %H:%М:%С",
)
logger = logging.getLogger("bot")

# Налаштування OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"

# Функція для взаємодії з OpenAI через URL
async def ask_openai(prompt: str, max_tokens: int = 500) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        }
        json_data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Ти є експертом Mobile Legends. Відповідай коротко і точно."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=json_data) as response:
                result = await response.json()
                return result['choices'][0]['message']['content'].strip()
    except aiohttp.ClientError as e:
        logger.error(f"HTTP error: {e}")
        return "Не вдалося отримати відповідь. Спробуйте пізніше."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Сталася непередбачувана помилка. Спробуйте пізніше."

# Окрема функція для створення бота і диспетчера
def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # Використання параметрів за замовчуванням
        session=AiohttpSession()  # Явна сесія для HTTP-запитів
    )
    dp = Dispatcher(storage=MemoryStorage())  # FSM сховище
    return bot, dp

# Основна функція запуску бота
async def main():
    logger.info("Starting bot...")
    bot, dp = create_bot_and_dispatcher()

    # Підключення обробників
    register_buttons_handlers(dp)
    register_navigation_handlers(dp)

    # Використання асинхронного контекстного менеджера
    try:
        async with bot:
            logger.info("Bot is polling...")
            await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")
    except Exception as e:
        logger.error("Critical error occurred: %s", e, exc_info=True)
    finally:
        logger.info("Closing bot session...")
        if bot.session:
            await bot.session.close()

# Точка входу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped gracefully!")
