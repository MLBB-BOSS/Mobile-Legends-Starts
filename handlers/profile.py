from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from io import BytesIO

# Функція для створення зображення профілю
async def generate_custom_profile(username, rating, matches, wins, losses):
    # Завантаження фону (замініть 'background.jpg' на ваш файл)
    bg = Image.open("background.jpg").resize((800, 600))  # Змінити розмір фону
    draw = ImageDraw.Draw(bg)

    # Шрифти
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        content_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = content_font = ImageFont.load_default()

    # Текст поверх фону
    draw.text((50, 50), "🔍 Ваш Профіль", fill="white", font=title_font)
    draw.text((50, 150), f"👤 @{username}", fill="cyan", font=content_font)
    draw.text((50, 200), f"🚀 Рейтинг: {rating}", fill="yellow", font=content_font)
    draw.text((50, 250), f"🎮 Матчі: {matches}", fill="white", font=content_font)
    draw.text((50, 300), f"🏆 Перемоги: {wins}", fill="green", font=content_font)
    draw.text((50, 350), f"❌ Поразки: {losses}", fill="red", font=content_font)

    # Генерація графіка
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot([10, 20, 15, 25], color="cyan", linewidth=3, marker="o")
    ax.set_title("Графік активності", color="white")
    ax.set_facecolor("black")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    buf = BytesIO()
    plt.savefig(buf, format="PNG", transparent=True)
    plt.close(fig)
    graph = Image.open(buf).resize((400, 200))
    
    # Вставлення графіка
    bg.paste(graph, (350, 400), mask=graph)

    # Збереження у пам'ять
    output = BytesIO()
    bg.save(output, format="PNG")
    output.seek(0)
    return output
