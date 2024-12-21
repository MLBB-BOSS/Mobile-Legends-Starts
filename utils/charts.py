# utils/charts.py

import io
import matplotlib.pyplot as plt

from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command

# Створюємо окремий Router для хендлерів, які стосуються графіків
charts_router = Router()

def generate_rating_chart(rating_history: list[int], figsize=(4, 4)) -> io.BytesIO:
    """
    Генерує графік зміни рейтингу.
    rating_history - список рейтингів по часу, наприклад: [100, 200, 250, 300].

    Повертає BytesIO, який містить PNG-зображення (щоб згодом відправити як photo).
    """
    if not rating_history or not all(isinstance(x, (int, float)) for x in rating_history):
        raise ValueError("rating_history must be a non-empty list of numbers")

    plt.figure(figsize=figsize)
    plt.plot(rating_history, marker='o', linestyle='-', color='blue')
    plt.title("Графік зміни рейтингу")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")

    # Записуємо результат у буфер пам’яті
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close()
    return buf

@charts_router.message(Command("my_progress"))
async def show_progress(message: Message):
    """
    Хендлер на команду /my_progress, який будує зразковий графік рейтингу
    та відправляє його користувачеві.
    """
    try:
        # Зразкові дані для прикладу
        rating_history = [100, 200, 250, 300]
        # Викликаємо функцію для генерації зображення з графіком
        chart = generate_rating_chart(rating_history)
        # Створюємо InputFile для надсилання в Telegram
        photo_file = InputFile(chart, filename="chart.png")
        profile_text = "Ваш прогрес за останні сеанси"

        await message.answer_photo(photo=photo_file, caption=profile_text)

    except Exception as e:
        await message.answer("Виникла помилка при створенні графіка.")
        # Перекидаємо помилку вище для логування або аналізу
        raise e
