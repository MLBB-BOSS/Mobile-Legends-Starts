# file: handlers/profile.py

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import logging

# Створення маршрутизатора (має бути до використання)
profile_router = Router()

# Функція для створення профілю
async def generate_full_profile(username, rating, matches, wins, losses):
    # Створюємо вертикальне полотно 9:16
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), "#0F0F0F")  # Чорний фон
    draw = ImageDraw.Draw(img)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        content_font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = content_font = small_font = ImageFont.load_default()

    # Заголовок
    draw.text((50, 50), "🔍 Профіль Гравця", fill="#FFFFFF", font=title_font)

    # Блок основної інформації (рамка)
    draw.rectangle([50, 150, width - 50, 450], outline="#007BFF", width=5, fill="#1E1E2E")
    draw.text((70, 180), f"👤 Ім'я користувача: @{username}", fill="#00CFFF", font=content_font)
    draw.text((70, 260), f"🚀 Рейтинг: {rating}", fill="#FFD700", font=content_font)
    draw.text((70, 340), f"🎮 Матчі: {matches}", fill="#FFFFFF", font=content_font)
    draw.text((500, 340), f"🏆 Перемоги: {wins}", fill="#28A745", font=content_font)
    draw.text((800, 340), f"❌ Поразки: {losses}", fill="#DC3545", font=content_font)

    # Генерація графіку
    fig, ax = plt.subplots(figsize=(6, 3), facecolor="#0F0F0F")
    ax.plot([1, 2, 3, 4, 5], [10, 15, 8, 20, 30], color="#00CFFF", linewidth=4, marker="o")
    ax.set_title("Графік активності", fontsize=14, color="white")
    ax.tick_params(colors="white")
    ax.grid(color="#333333")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставка графіка на полотно
    graph = Image.open(buf).resize((900, 500))
    img.paste(graph, (90, 500), mask=graph)

    # Збереження у буфер
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Обробник для команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message):
    try:
        username = message.from_user.username or "Unknown"
        profile_image = await generate_full_profile(username, 100, 20, 50, 5)

        input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
        await message.answer_photo(photo=input_file, caption="🖼 Ваш профіль")
    except Exception as e:
        logging.error(f"Помилка у створенні профілю: {e}")
        await message.answer("❌ Виникла помилка при створенні профілю.")