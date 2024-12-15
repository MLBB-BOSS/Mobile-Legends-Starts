from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from aiogram.types import BufferedInputFile

async def generate_profile_image(username, rating, matches, wins, losses):
    # Створення зображення 800x500 з блакитним фоном
    img = Image.new("RGB", (800, 500), "#E0F7FA")  # Колір фону (блакитний)
    draw = ImageDraw.Draw(img)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)  # Більший заголовок
        content_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = content_font = ImageFont.load_default()

    # Додавання заголовка
    draw.text((20, 20), "🔍 Ваш Профіль", fill="black", font=title_font)

    # Основна інформація з більшим відступом
    draw.text((20, 100), f"👤 Ім'я користувача: @{username}", fill="blue", font=content_font)
    draw.text((20, 150), f"🚀 Рейтинг: {rating}", fill="black", font=content_font)
    draw.text((20, 200), f"🎮 Матчі: {matches}", fill="black", font=content_font)
    draw.text((20, 250), f"🏆 Перемоги: {wins}", fill="green", font=content_font)
    draw.text((20, 300), f"❌ Поразки: {losses}", fill="red", font=content_font)

    # Підсумковий текст
    draw.text((20, 420), "🕒 Останнє оновлення: 2024-12-15 08:11:39", fill="gray", font=content_font)

    # Додавання рамки
    draw.rectangle([10, 10, 790, 490], outline="black", width=3)

    # Збереження у пам'ять
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
