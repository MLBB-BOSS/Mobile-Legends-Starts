from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import matplotlib.pyplot as plt
from aiogram.types import Message, BufferedInputFile
from aiogram import Router
from aiogram.filters import Command
import logging

profile_router = Router()

# Функція для створення профілю
async def generate_detailed_profile(username, fullname, level, activity, rating, matches, wins, losses):
    # Полотно 9:16
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
    draw.text((50, 30), "🎮 Профіль Гравця", fill="#FFD700", font=title_font)

    # Блок загальної інформації
    draw.rectangle([50, 120, width - 50, 400], outline="#007BFF", width=5, fill="#1E1E2E")
    draw.text((70, 150), f"👤 Нікнейм: @{username}", fill="#00CFFF", font=content_font)
    draw.text((70, 220), f"📝 Ім'я: {fullname}", fill="#FFFFFF", font=content_font)
    draw.text((70, 290), f"⭐ Рівень: {level}   🔥 Активність: {activity}%", fill="#FFD700", font=content_font)

    # Блок статистики
    draw.rectangle([50, 450, width - 50, 700], outline="#28A745", width=5, fill="#1E1E2E")
    draw.text((70, 480), f"🚀 Рейтинг: {rating}", fill="#FFD700", font=content_font)
    draw.text((70, 550), f"🎮 Матчі: {matches}", fill="#FFFFFF", font=content_font)
    draw.text((500, 550), f"🏆 Перемоги: {wins}", fill="#28A745", font=content_font)
    draw.text((800, 550), f"❌ Поразки: {losses}", fill="#DC3545", font=content_font)

    # Генерація графіка активності
    fig, ax = plt.subplots(figsize=(5, 3), facecolor="#0F0F0F")
    ax.plot([1, 2, 3, 4, 5], [activity, 50, 60, 70, 80], color="#00CFFF", linewidth=4, marker="o")
    ax.set_title("📈 Графік активності", fontsize=14, color="white")
    ax.tick_params(colors="white")
    ax.grid(color="#333333")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставлення графіка
    graph = Image.open(buf).resize((900, 500))
    img.paste(graph, (90, 750), mask=graph)

    # Підсумок
    draw.text((50, 1300), "🎯 Ваш прогрес зростає! Продовжуйте в тому ж дусі!", fill="#FFFFFF", font=small_font)

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
        fullname = "Іван Іванов"
        level = 15
        activity = 87
        rating = 1200
        matches = 45
        wins = 30
        losses = 15

        profile_image = await generate_detailed_profile(username, fullname, level, activity, rating, matches, wins, losses)

        input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
        await message.answer_photo(photo=input_file, caption="🖼 Детальний профіль")
    except Exception as e:
        logging.error(f"Помилка у створенні профілю: {e}")
        await message.answer("❌ Виникла помилка при створенні профілю.")