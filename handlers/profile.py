# handlers/profile.py

import logging
from io import BytesIO
from typing import Optional

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.pyplot as plt
import aiohttp

from config import settings  # Ваш файл конфігурації
from database import get_db  # Ваш файл налаштувань бази даних
from models.user import User  # Модель користувача
from models.user_stats import UserStats  # Модель статистики користувача

# Ініціалізація маршрутизатора
profile_router = Router()

# Налаштування логування
logger = logging.getLogger(__name__)

# Функція для визначення рангу на основі рейтингу
def get_rank(rating: int) -> (str, str):
    if rating < 1000:
        return ("Bronze", "#CD7F32")
    elif 1000 <= rating < 2000:
        return ("Silver", "#C0C0C0")
    elif 2000 <= rating < 3000:
        return ("Gold", "#FFD700")
    elif 3000 <= rating < 4000:
        return ("Platinum", "#E5E4E2")
    elif 4000 <= rating < 5000:
        return ("Diamond", "#B9F2FF")
    else:
        return ("Master", "#FF4500")

# Функція для отримання аватарки користувача з Telegram
async def get_user_avatar(bot: Bot, telegram_id: int) -> Optional[Image.Image]:
    try:
        user_photos = await bot.get_user_profile_photos(user_id=telegram_id, limit=1)
        if user_photos.total_count > 0:
            photo = user_photos.photos[0][-1]  # Отримуємо найвищу роздільну здатність
            file_info = await bot.get_file(photo.file_id)
            file_path = file_info.file_path
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}') as resp:
                    if resp.status == 200:
                        img_bytes = await resp.read()
                        avatar = Image.open(BytesIO(img_bytes)).convert("RGBA").resize((200, 200))
                        # Додавання круглого маскування
                        mask = Image.new("L", avatar.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + avatar.size, fill=255)
                        avatar.putalpha(mask)
                        return avatar
    except Exception as e:
        logger.error(f"Помилка при завантаженні аватарки: {e}")
    return None

# Функція для створення профілю
async def generate_detailed_profile(user: User, stats: UserStats, bot: Bot) -> BytesIO:
    # Розміри зображення
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), "#0F0F0F")  # Темний фон
    draw = ImageDraw.Draw(img)

    # Завантаження шрифтів
    try:
        title_font = ImageFont.truetype("fonts/Arial-Bold.ttf", 60)
        header_font = ImageFont.truetype("fonts/Arial-Bold.ttf", 50)
        content_font = ImageFont.truetype("fonts/Arial.ttf", 40)
        small_font = ImageFont.truetype("fonts/Arial.ttf", 30)
    except IOError:
        # Використання стандартних шрифтів, якщо arial не знайдено
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Заголовок
    draw.text((50, 30), "🎮 Профіль Гравця", fill="#FFD700", font=title_font)

    # Загальна інформація
    info_box_coords = [50, 120, width - 50, 400]
    draw.rectangle(info_box_coords, outline="#007BFF", width=5, fill="#1E1E2E")
    draw.text((70, 150), f"👤 Нікнейм: @{user.username or 'Невідомо'}", fill="#00CFFF", font=content_font)
    draw.text((70, 220), f"📝 Ім'я: {user.fullname or 'Невідомо'}", fill="#FFFFFF", font=content_font)
    draw.text((70, 290), f"⭐ Рівень: {user.level}   🔥 Активність: {stats.activity}%", fill="#FFD700", font=content_font)

    # Додаткова статистика
    win_rate = (stats.wins / stats.matches) * 100 if stats.matches > 0 else 0
    draw.text((70, 360), f"🏅 Рейтинг: {stats.rating}", fill="#FFD700", font=content_font)
    draw.text((70, 430), f"🎮 Матчі: {stats.matches}", fill="#FFFFFF", font=content_font)
    draw.text((500, 430), f"🏆 Перемоги: {stats.wins}", fill="#28A745", font=content_font)
    draw.text((800, 430), f"❌ Поразки: {stats.losses}", fill="#DC3545", font=content_font)
    draw.text((500, 360), f"📈 Win Rate: {win_rate:.2f}%", fill="#28A745", font=content_font)

    # Система Рейтингів
    rank, color = get_rank(stats.rating)
    rank_text = f"🏅 Ранг: {rank}"
    text_width, _ = draw.textsize(rank_text, font=header_font)
    draw.text((width // 2 - text_width // 2, 150), rank_text, fill=color, font=header_font)

    # Генерація графіка активності
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor="#0F0F0F")
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    # Припустимо, що у UserStats є поле activity_history, яке є списком значень
    # Наприклад: "activity_history" = "70,75,80,85,90,95,100"
    if stats.activity_history:
        activity_data = list(map(float, stats.activity_history.split(',')))
    else:
        activity_data = [50, 60, 70, 80, 65, 75, 85]
    ax.plot(days, activity_data, color="#00CFFF", linewidth=4, marker="o", markersize=10, markerfacecolor="#FFD700")
    ax.set_title("📈 Графік Активності", fontsize=20, color="white")
    ax.set_facecolor("#0F0F0F")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    ax.grid(color="#333333")

    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставлення графіка
    graph = Image.open(buf).resize((900, 500))
    img.paste(graph, (90, 750), mask=graph)

    # Аватарка користувача
    avatar = await get_user_avatar(bot, user.telegram_id)
    if avatar:
        img.paste(avatar, (width // 2 - 100, 300), mask=avatar)
    else:
        try:
            default_avatar = Image.open("default_avatar.png").convert("RGBA").resize((200, 200))
            # Додавання круглого маскування для заглушки
            mask = Image.new("L", default_avatar.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0) + default_avatar.size, fill=255)
            default_avatar.putalpha(mask)
            img.paste(default_avatar, (width // 2 - 100, 300), mask=default_avatar)
        except IOError:
            logger.warning("Аватарка користувача не знайдена. Використовується заглушка.")

    # Рейтингові піктограми
    try:
        rank_icon = Image.open(f"icons/{rank.lower()}.png").convert("RGBA").resize((100, 100))
        img.paste(rank_icon, (width - 150, 120), mask=rank_icon)
    except IOError:
        logger.warning(f"Піктограма для рангу {rank} не знайдена.")

    # Прогрес
    draw.text((50, 1300), "🎯 Ваш прогрес зростає! Продовжуйте в тому ж дусі!", fill="#FFFFFF", font=small_font)

    # Додаткові декоративні елементи (опціонально)
    # Наприклад, додати лінії, іконки або інші графічні елементи для покращення вигляду

    # Збереження у буфер
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, session: AsyncSession, bot: Bot):
    try:
        telegram_id = message.from_user.id
        username = message.from_user.username or "Невідомо"
        fullname = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip() or "Невідомо"

        # Отримання користувача з бази даних
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none()

        if not user:
            # Якщо користувача немає в базі даних, створіть його
            user = User(
                telegram_id=telegram_id,
                username=username,
                fullname=fullname
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # Отримання або створення статистики користувача
        stmt = select(UserStats).where(UserStats.user_id == user.id)
        result = await session.execute(stmt)
        stats: Optional[UserStats] = result.scalar_one_or_none()

        if not stats:
            stats = UserStats(user_id=user.id)
            session.add(stats)
            await session.commit()
            await session.refresh(stats)

        # Генерація профілю
        profile_image = await generate_detailed_profile(user, stats, bot)
        input_file = BufferedInputFile(profile_image.read(), filename="profile.png")

        # Формування HTML-форматованого тексту
        profile_text = (
            f"<b>🔎 Ваш Профіль:</b>\n\n"
            f"🏅 <b>Ім'я користувача:</b> @{user.username or 'Невідомо'}\n"
            f"🚀 <b>Рівень:</b> {stats.rating // 100}\n"
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