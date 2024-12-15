from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import matplotlib.pyplot as plt

# Функція для створення кастомного профілю
async def generate_custom_profile(username: str, rating: int, matches: int, wins: int, losses: int):
    # Створення фону
    img = Image.new("RGB", (800, 1000), "#f8f9fa")  # Світло-сірий фон
    draw = ImageDraw.Draw(img)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        content_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = content_font = ImageFont.load_default()

    # Заголовок
    draw.text((50, 30), "🔍 Профіль Гравця", fill="#333333", font=title_font)

    # Інформація
    y_offset = 150
    spacing = 70
    draw.text((50, y_offset), f"👤 Ім'я користувача: @{username}", fill="#007BFF", font=content_font)
    draw.text((50, y_offset + spacing), f"🚀 Рейтинг: {rating}", fill="#212529", font=content_font)
    draw.text((50, y_offset + 2 * spacing), f"🎮 Матчі: {matches}", fill="#212529", font=content_font)
    draw.text((50, y_offset + 3 * spacing), f"🏆 Перемоги: {wins}", fill="#28A745", font=content_font)
    draw.text((50, y_offset + 4 * spacing), f"❌ Поразки: {losses}", fill="#DC3545", font=content_font)

    # Генерація графіку
    fig, ax = plt.subplots(figsize=(5, 3), facecolor="#f8f9fa")
    ax.plot([10, 20, 30, 40, 50], [5, 15, 25, 10, 30], color="#007BFF", linewidth=3, marker="o")
    ax.set_title("Графік активності", fontsize=10, color="#333333")
    ax.grid(True, color="#DDDDDD")
    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)

    # Вставка графіку у зображення
    graph = Image.open(buf).resize((500, 300))
    img.paste(graph, (150, y_offset + 5 * spacing))

    # Збереження у буфер
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# Функція для виклику у боті
@profile_router.message(Command("profile"))
async def show_profile(message: Message):
    username = message.from_user.username or "Unknown"
    profile_image = await generate_custom_profile(username, 100, 20, 15, 5)

    input_file = BufferedInputFile(profile_image.read(), filename="profile.png")
    await message.answer_photo(photo=input_file, caption="🖼 Ваш профіль")