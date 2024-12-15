# file: handlers/profile.py

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import logging

# Створення маршрутизатора
profile_router = Router()

# Функція для створення кастомного профілю
async def generate_custom_profile(username: str, rating: int, matches: int, wins: int, losses: int):
    # Створюємо зображення білого фону
    img = Image.new("RGB", (800, 1000), "white")
    draw = ImageDraw.Draw(img)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        content_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = content_font = ImageFont.load_default()

    # Додавання заголовку
    draw.text((50, 30), "🔍 Профіль Гравця", fill="black", font=title_font)

    # Основна інформація
    draw.text((50, 150), f"👤 Ім'я користувача: @{username}", fill="blue", font=content_font)
    draw.text((50, 220), f"🚀 Рейтинг: {rating}", fill="black", font=content_font)
    draw.text((50, 290), f"🎮 Матчі: {matches}", fill="black", font=content_font)
    draw.text((50, 360), f"🏆 Перемоги: {wins}", fill="green", font=content_font)
    draw.text((50, 430), f"❌ Поразки: {losses}", fill="red", font=content_font)

    # Генерація графіку
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot([10, 20, 30, 40, 50], [5, 15, 25, 10, 30], color="blue", linewidth=2, marker="o")
    ax.set_facecolor("white")
    ax.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)
    graph = Image.open(buf).resize((400, 200))
    img.paste(graph, (350, 500))

    # Збереження зображення у буфер
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Обробник команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message):
    try:
        username = message.from_user.username or "Unknown"
        profile_image = await generate_custom_profile(username, 100, 20, 15, 5)

        input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
        await message.answer_photo(photo=input_file, caption="🖼 Ваш профіль")
    except Exception as e:
        logging.error(f"Помилка при створенні профілю: {e}")
        await message.answer("❌ Сталася помилка під час створення профілю.")
