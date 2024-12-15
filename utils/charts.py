import io
import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command

router = Router()

# Функція для генерації графіка
def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    """
    Генерує графік зміни рейтингу.
    rating_history - список рейтингів по часу, наприклад: [100, 200, 250, 300].
    """
    plt.figure(figsize=(4, 4))
    plt.plot(rating_history, marker='o')
    plt.title("Графік зміни рейтингу")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

# Обробник команди
@router.message(Command("my_progress"))
async def show_progress(message: Message):
    rating_history = [100, 200, 250, 300]  # Зразкові дані
    chart = generate_rating_chart(rating_history)  # Генеруємо графік

    # Обгортаємо BytesIO в InputFile
    photo_file = InputFile(chart, filename="chart.png")
    profile_text = "Ваш прогрес за останні сеанси"

    # Відправляємо графік
    await message.answer_photo(photo=photo_file, caption=profile_text)