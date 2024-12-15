# file: handlers/profile.py

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging

# Створення Router
profile_router = Router()

# Функція для створення зображення профілю
async def generate_profile_image(username, rating, matches, wins, losses):
    # Створення зображення 600x400 з білим фоном
    img = Image.new("RGB", (600, 400), "white")
    draw = ImageDraw.Draw(img)

    # Шрифти (використовуйте свій шрифт, наприклад, Arial)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        content_font = ImageFont.truetype("arial.ttf", 22)
    except:
        title_font = content_font = ImageFont.load_default()

    # Додавання заголовка
    draw.text((20, 20), "🔍 Ваш Профіль", fill="black", font=title_font)

    # Основна інформація
    draw.text((20, 80), f"👤 Ім'я користувача: @{username}", fill="blue", font=content_font)
    draw.text((20, 120), f"🚀 Рейтинг: {rating}", fill="black", font=content_font)
    draw.text((20, 160), f"🎮 Матчі: {matches}", fill="black", font=content_font)
    draw.text((20, 200), f"🏆 Перемоги: {wins}", fill="green", font=content_font)
    draw.text((20, 240), f"❌ Поразки: {losses}", fill="red", font=content_font)

    # Нижній підсумковий текст
    draw.text((20, 340), "🕒 Останнє оновлення: 2024-12-15 08:11:39", fill="gray", font=content_font)

    # Збереження у пам'ять
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# Обробник команди /profile
@profile_router.message(Command("profile"))
async def show_profile(message: Message):
    try:
        # Дані користувача
        username = message.from_user.username or "Невідомий користувач"
        rating = 100
        matches = 10
        wins = 7
        losses = 3

        # Генерація зображення профілю
        profile_img = await generate_profile_image(username, rating, matches, wins, losses)

        # Підготовка до відправки зображення
        input_file = BufferedInputFile(profile_img.read(), filename="profile.png")

        # Відправлення зображення з підписом
        await message.answer_photo(photo=input_file, caption="🖼 <b>Ваш профіль</b>", parse_mode="HTML")
    except Exception as e:
        logging.error(f"Помилка при створенні профілю: {e}")
        await message.answer("❌ Сталася помилка під час створення профілю.")