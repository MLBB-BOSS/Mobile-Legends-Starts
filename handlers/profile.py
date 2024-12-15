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

from database import get_db  # Функція для доступу до бази даних

# Ініціалізація логування
logger = logging.getLogger(__name__)

# Ініціалізація маршрутизатора
profile_router = Router()

# Налаштування ORM моделі
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
    messages_sent = Column(Integer, default=0)
    rating_rank = Column(String, default="Bronze")

# Функція для визначення рангу
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

# Функція для створення графічного профілю
async def generate_profile_image(user: User) -> BytesIO:
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), "#1C1C1C")
    draw = ImageDraw.Draw(img)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        content_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = content_font = ImageFont.load_default()

    # Заголовок
    draw.text((width // 2 - 200, 30), "🎮 Профіль Гравця", fill="#FFD700", font=title_font)

    # Основна інформація
    draw.text((70, 150), f"👤 Нікнейм: @{user.username}", fill="#00CFFF", font=content_font)
    draw.text((70, 220), f"📝 Ім'я: {user.fullname}", fill="#FFFFFF", font=content_font)
    draw.text((70, 290), f"⭐ Рівень: {user.level}", fill="#FFD700", font=content_font)
    draw.text((70, 360), f"🔥 Активність: {user.activity}%", fill="#FFD700", font=content_font)

    # Статистика
    draw.text((70, 450), f"🚀 Рейтинг: {user.rating}", fill="#FFD700", font=content_font)
    draw.text((70, 520), f"🎮 Матчі: {user.matches}", fill="#FFFFFF", font=content_font)
    draw.text((70, 590), f"🏆 Перемоги: {user.wins}", fill="#28A745", font=content_font)
    draw.text((70, 660), f"❌ Поразки: {user.losses}", fill="#DC3545", font=content_font)

    # Графік активності
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#1C1C1C")
    activity_data = [user.activity, 50, 60, 70, 80, 65, 75]
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    ax.plot(days, activity_data, color="#00CFFF", linewidth=4, marker="o")
    ax.set_title("📈 Графік Активності", fontsize=16, color="white")
    ax.tick_params(colors="white")
    ax.grid(color="#333333")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставка графіка
    graph = Image.open(buf).resize((900, 500))
    img.paste(graph, (90, 750), mask=graph)

    # Збереження зображення
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Обробник команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message, bot: Bot):
    try:
        telegram_id = message.from_user.id

        # Отримання сесії бази даних
        async for session in get_db():
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user: Optional[User] = result.scalar_one_or_none()

            # Якщо користувача немає
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=message.from_user.username or "Unknown",
                    fullname=message.from_user.full_name,
                    level=1,
                    activity=0.0,
                    rating=0,
                    matches=0,
                    wins=0,
                    losses=0
                )
                session.add(user)
                await session.commit()

            # Генерація профілю
            profile_image = await generate_profile_image(user)
            input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
            await message.answer_photo(photo=input_file, caption="🖼 Ваш Профіль")
    except Exception as e:
        logger.error(f"Помилка у створенні профілю: {e}")
        await message.answer("❌ Виникла помилка під час створення профілю.")
