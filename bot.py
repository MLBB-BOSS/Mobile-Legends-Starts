import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import settings
from handlers.base import setup_handlers
from utils.db import engine
from models.base import Base
import models.user
import models.user_stats
import plotly.graph_objects as go
from io import BytesIO

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

# Ініціалізація диспетчера
dp = Dispatcher(storage=MemoryStorage())


async def create_tables():
    """Створює таблиці у базі даних, якщо вони ще не існують."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")


def generate_rating_chart(rating_history):
    """Генерує графік рейтингу у вигляді зображення."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=rating_history,
        x=list(range(len(rating_history))),
        mode='lines+markers',
        line=dict(color='#00FFEA', width=3),
        marker=dict(size=12, color='#FF5733', line=dict(width=2, color='#FFD700'))
    ))

    fig.update_layout(
        title="Ігрова статистика рейтингу",
        title_font=dict(size=22, color='#FF5733'),
        xaxis=dict(title='Період', title_font=dict(size=14, color='#00FFEA')),
        yaxis=dict(title='Рейтинг', title_font=dict(size=14, color='#00FFEA')),
        template='plotly_dark'
    )

    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png', engine='kaleido')
    img_bytes.seek(0)
    return img_bytes


async def set_bot_commands(bot: Bot):
    """Встановлює команди для бота у навігаційному меню."""
    commands = [
        BotCommand(command="help", description="Отримати довідку"),
        BotCommand(command="profile", description="Переглянути ваш профіль"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Bot commands set successfully: %s", commands)


async def main():
    logger.info("Starting bot...")
    try:
        await create_tables()
        await set_bot_commands(bot)
        setup_handlers(dp)

        # Логування підключених роутерів
        logger.info("Registered routers successfully.")

        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        if bot.session:
            await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
