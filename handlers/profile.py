import logging
from io import BytesIO
from typing import Optional

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

from config import settings  # Ваш файл конфігурації
from database import get_db  # Ваш файл налаштувань бази даних

# Налаштування бази даних
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    fullname = Column(String)
    level = Column(Integer, default=1)
    activity = Column(Float, default=0.0)
    rating = Column(Integer, default=0)
    matches = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)
    active_days = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    rating_rank = Column(String, default="Bronze")
    achievements_count = Column(Integer, default=0)
    # Додайте інші поля за потребою

# Ініціалізація маршрутизатора
profile_router = Router()

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

# Функція для створення профілю
async def generate_detailed_profile(user: User) -> BytesIO:
    # Розміри зображення
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), "#1C1C1C")  # Темний фон
    draw = ImageDraw.Draw(img)

    # Завантаження шрифтів
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        header_font = ImageFont.truetype("arial.ttf", 50)
        content_font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        # Використання стандартних шрифтів, якщо arial не знайдено
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Заголовок
    draw.text((width // 2 - 200, 30), "🎮 Профіль Гравця", fill="#FFD700", font=title_font)

    # Загальна інформація
    info_box_coords = [50, 120, width - 50, 400]
    draw.rectangle(info_box_coords, outline="#007BFF", width=5, fill="#2E2E3E")
    draw.text((70, 150), f"👤 Нікнейм: @{user.username}", fill="#00CFFF", font=content_font)
    draw.text((70, 220), f"📝 Ім'я: {user.fullname}", fill="#FFFFFF", font=content_font)
    draw.text((70, 290), f"⭐ Рівень: {user.level}", fill="#FFD700", font=content_font)
    draw.text((500, 290), f"🔥 Активність: {user.activity}%", fill="#FFD700", font=content_font)

    # Додаткова статистика
    win_rate = (user.wins / user.matches) * 100 if user.matches > 0 else 0
    draw.text((70, 360), f"🏅 Рейтинг: {user.rating}", fill="#FFD700", font=content_font)
    draw.text((70, 430), f"🎮 Матчі: {user.matches}", fill="#FFFFFF", font=content_font)
    draw.text((500, 430), f"🏆 Перемоги: {user.wins}", fill="#28A745", font=content_font)
    draw.text((800, 430), f"❌ Поразки: {user.losses}", fill="#DC3545", font=content_font)
    draw.text((500, 360), f"📈 Win Rate: {win_rate:.2f}%", fill="#28A745", font=content_font)

    # Система Рейтингів
    rank, color = get_rank(user.rating)
    rank_text = f"🏅 Ранг: {rank}"
    text_width, _ = draw.textsize(rank_text, font=header_font)
    draw.text((width // 2 - text_width // 2, 150), rank_text, fill=color, font=header_font)

    # Генерація графіка активності
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor="#1C1C1C")
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    # Замініть ці дані на реальні дані активності користувача
    activity_data = [user.activity, 50, 60, 70, 80, 65, 75]
    ax.plot(days, activity_data, color="#00CFFF", linewidth=4, marker="o")
    ax.set_title("📈 Графік Активності", fontsize=20, color="white")
    ax.set_facecolor("#1C1C1C")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    ax.grid(color="#333333")

    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставлення графіка
    graph = Image.open(buf).resize((900, 500))
    img.paste(graph, (90, 500), mask=graph)

    # Прогрес
    draw.text((50, 1050), "🎯 Ваш прогрес зростає! Продовжуйте в тому ж дусі!", fill="#FFFFFF", font=small_font)

    # Рейтингові піктограми
    try:
        rank_icon = Image.open(f"icons/{rank.lower()}.png").resize((100, 100))
        img.paste(rank_icon, (width - 150, 120), mask=rank_icon)
    except IOError:
        logging.warning(f"Піктограма для рангу {rank} не знайдена.")
    
    # Аватарка користувача
    try:
        # Якщо у вас є аватарка користувача, завантажте її з Telegram
        # Для простоти використовується заглушка
        avatar = Image.open("default_avatar.png").resize((200, 200))
        img.paste(avatar, (width // 2 - 100, 300), mask=avatar)
    except IOError:
        logging.warning("Аватарка користувача не знайдена. Використовується заглушка.")
    
    # Збереження зображення у буфер
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, session: AsyncSession, bot: Bot):
    try:
        telegram_id = message.from_user.id
        # Отримання користувача з бази даних
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none()

        if not user:
            # Якщо користувача немає в базі даних, створіть його або відправте повідомлення
            user = User(
                telegram_id=telegram_id,
                username=message.from_user.username or "Unknown",
                fullname=f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip(),
                level=1,
                activity=0.0,
                rating=0,
                matches=0,
                wins=0,
                losses=0,
                screenshot_count=0,
                mission_count=0,
                quiz_count=0,
                active_days=0,
                messages_sent=0,
                rating_rank="Bronze",
                achievements_count=0
            )
            session.add(user)
            await session.commit()
        
        # Генерація профілю
        profile_image = await generate_detailed_profile(user)
        input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
        
        # Відправка зображення користувачу
        await message.answer_photo(photo=input_file, caption="🖼 Ваш Детальний Профіль")
    except Exception as e:
        logging.error(f"Помилка у створенні профілю: {e}")
        await message.answer("❌ Виникла помилка при створенні профілю.")