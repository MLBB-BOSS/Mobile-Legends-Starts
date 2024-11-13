# services/screenshot_service.py

import logging
from aiogram import types
from database.connection import get_db
from models.screenshot import Screenshot
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

async def handle_screenshot_upload(message: types.Message):
    """Обробка завантаження скріншоту користувачем"""
    if not message.photo:
        await message.reply("Будь ласка, надішліть фотографію.")
        return

    photo = message.photo[-1]  # Вибираємо найвищу якість
    file_id = photo.file_id
    user_id = message.from_user.id

    async for session in get_db():
        # Перевірка, чи вже існує скріншот з таким file_id
        stmt = select(Screenshot).where(Screenshot.file_id == file_id)
        result = await session.execute(stmt)
        existing_screenshot = result.scalars().first()

        if existing_screenshot:
            await message.reply("Цей скріншот вже був завантажений.")
            return

        # Створення нового запису
        new_screenshot = Screenshot(
            user_id=user_id,
            file_id=file_id
        )
        session.add(new_screenshot)
        await session.commit()
        await message.reply("Скріншот успішно завантажено!")

async def get_leaderboard():
    """Отримання таблиці лідерів за кількістю скріншотів"""
    async for session in get_db():
        stmt = select(Screenshot.user_id, func.count(Screenshot.id).label("count")) \
            .group_by(Screenshot.user_id) \
            .order_by(func.count(Screenshot.id).desc()) \
            .limit(10)
        result = await session.execute(stmt)
        leaderboard = result.all()

        leaderboard_text = "🏆 <b>Таблиця Лідерів</b>\n\n"
        for rank, (user_id, count) in enumerate(leaderboard, start=1):
            leaderboard_text += f"{rank}. User ID: {user_id} - {count} скріншотів\n"

        return leaderboard_text

async def get_user_profile(user_id: int):
    """Отримання профілю користувача"""
    async for session in get_db():
        stmt = select(func.count(Screenshot.id)).where(Screenshot.user_id == user_id)
        result = await session.execute(stmt)
        count = result.scalar()

        profile_text = (
            f"👤 <b>Профіль Користувача</b>\n\n"
            f"User ID: {user_id}\n"
            f"Кількість завантажених скріншотів: {count}"
        )
        return profile_text

async def get_hero_info():
    """Отримання інформації про героїв"""
    # Приклад статичної інформації, можна розширити
    heroes_info = (
        "<b>Інформація про Героїв</b>\n\n"
        "1. Assassin - швидкий та смертельний.\n"
        "2. Fighter - збалансований бійник.\n"
        "3. Mage - магічний потужний.\n"
        "4. Marksman - дальній бій.\n"
        "5. Support - підтримка команди.\n"
        "6. Tank - витривалий та стійкий."
    )
    return heroes_info
