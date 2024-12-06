# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from config import settings
from handlers.base import setup_handlers
import openai  # Інтеграція OpenAI

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bot")

# Налаштування OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Функція для взаємодії з OpenAI
async def ask_openai(prompt: str, max_tokens: int = 500) -> str:
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ти є експертом Mobile Legends. Відповідай коротко і точно."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.7,  # Налаштування креативності
            )
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return "Не вдалося отримати відповідь. Спробуйте пізніше."

# Окрема функція для створення бота і диспетчера
def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()  # Явна сесія для HTTP-запитів
    )
    dp = Dispatcher(storage=MemoryStorage())  # FSM сховище
    return bot, dp

# Основна функція запуску бота
async def main():
    logger.info("Starting bot...")
    bot, dp = create_bot_and_dispatcher()

    # Підключення обробників
    setup_handlers(dp)

    # Команда для OpenAI інтеграції
    @dp.message(Command("ai"))
    async def handle_openai_request(message: Message):
        user_prompt = message.text.split(maxsplit=1)[-1]  # Отримуємо текст після команди
        if not user_prompt or user_prompt == "/ai":
            await message.answer("Введіть текст запиту після команди /ai.")
            return

        await message.answer("Запит обробляється, зачекайте...")
        response = await ask_openai(user_prompt)  # Виклик функції OpenAI
        await message.answer(response)

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
