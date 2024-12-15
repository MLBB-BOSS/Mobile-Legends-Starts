# handlers/profile.py

import logging
from io import BytesIO
from typing import Optional
import os

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.pyplot as plt
import aiohttp

from config import settings  # Ваш файл конфігурації
from models.user import User  # Модель користувача
from models.user_stats import UserStats  # Модель статистики користувача
from utils.db import AsyncSessionLocal  # Імпортуємо AsyncSessionLocal

# Ініціалізація маршрутизатора
profile_router = Router()

# Налаштування логування
logger = logging.getLogger(__name__)

# Інші функції та обробники...

# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, bot: Bot):
    try:
        async with AsyncSessionLocal() as db:
            telegram_id = message.from_user.id
            username = message.from_user.username or "Невідомо"
            fullname = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip() or "Невідомо"

            # Отримання користувача з бази даних
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await db.execute(stmt)
            user: Optional[User] = result.scalar_one_or_none()

            if not user:
                # Якщо користувача немає в базі даних, створіть його
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    fullname=fullname
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)

            # Отримання або створення статистики користувача
            stmt = select(UserStats).where(UserStats.user_id == user.id)
            result = await db.execute(stmt)
            stats: Optional[UserStats] = result.scalar_one_or_none()

            if not stats:
                stats = UserStats(user_id=user.id)
                db.add(stats)
                await db.commit()
                await db.refresh(stats)

            # Генерація профілю
            profile_image = await generate_detailed_profile(user, stats, bot)
            input_file = BufferedInputFile(profile_image.read(), filename="profile.png")

            # Формування HTML-форматованого тексту
            profile_text = (
                f"<b>🔎 Ваш Профіль:</b>\n\n"
                f"🏅 <b>Ім'я користувача:</b> @{user.username or 'Невідомо'}\n"
                f"🚀 <b>Рівень:</b> {user.level}\n"
                f"📈 <b>Рейтинг:</b> {stats.rating}\n"
                f"🎯 <b>Досягнення:</b> {stats.achievements_count} досягнень\n"
                f"🎮 <b>Матчі:</b> {stats.total_matches}\n"
                f"🏆 <b>Перемоги:</b> {stats.total_wins}\n"
                f"❌ <b>Поразки:</b> {stats.total_losses}\n"
                f"\n📅 <i>Останнє оновлення:</i> {stats.last_update.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Відправка зображення та тексту
            await message.answer_photo(photo=input_file, caption=profile_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Помилка у створенні профілю: {e}")
        await message.answer("❌ Виникла помилка при створенні профілю.")