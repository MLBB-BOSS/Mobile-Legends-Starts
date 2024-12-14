# utils/charts.py
import io
from PIL import Image, ImageDraw, ImageFont

def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    """
    Генерує графік зміни рейтингу.
    rating_history - список рейтингів по часу, наприклад: [100, 200, 250, 300].
    """
    width, height = 500, 300
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Налаштування шрифтів
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    # Визначення максимального рейтингу для масштабування
    max_rating = max(rating_history) + 20
    step_x = (width - 100) // (len(rating_history) - 1) if len(rating_history) > 1 else width - 100
    step_y = (height - 100) / max_rating

    # Малюємо осі
    draw.line([(50, 50), (50, height - 50)], fill='black')  # Y-вісь
    draw.line([(50, height - 50), (width - 50, height - 50)], fill='black')  # X-вісь

    # Малюємо лінії рейтингу
    for i in range(1, len(rating_history)):
        x1 = 50 + (i - 1) * step_x
        y1 = height - 50 - rating_history[i - 1] * step_y
        x2 = 50 + i * step_x
        y2 = height - 50 - rating_history[i] * step_y
        draw.line([(x1, y1), (x2, y2)], fill='blue', width=2)

    # Малюємо точки рейтингу
    for i, rating in enumerate(rating_history):
        x = 50 + i * step_x
        y = height - 50 - rating * step_y
        draw.ellipse([(x-5, y-5), (x+5, y+5)], fill='red', outline='black')
        # Додаємо текст рейтингу
        draw.text((x-10, y-25), str(rating), font=font, fill='black')

    # Додаємо підписи осей
    try:
        font_large = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font_large = ImageFont.load_default()

    draw.text((width//2 - 30, height - 30), "Сеанс", font=font_large, fill='black')
    draw.text((10, height//2 - 40), "Рейтинг", font=font_large, fill='black')

    # Зберігаємо зображення у BytesIO
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io