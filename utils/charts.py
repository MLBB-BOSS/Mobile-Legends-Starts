import io
import matplotlib.pyplot as plt

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command  # Імпорт для фільтра команд

charts_router = Router()

# Додатковий хендлер для обробки команди "/chart"
@charts_router.message(Command("chart"))
async def send_chart(message: Message):
    """
    Відправляє графік користувачу.
    """
    try:
        # Зразкові дані для графіка
        data = [10, 20, 30, 40, 50]
        chart = create_chart(data, title="Приклад графіка")

        # Відправка графіка користувачу
        await message.answer_photo(photo=chart, caption="Ось ваш графік!")
    except Exception as e:
        await message.answer("Не вдалося створити графік.")
        raise e

def create_chart(data: list[int], title: str = "Default Title") -> io.BytesIO:
    """
    Створює простий графік на основі переданих даних.
    """
    if not data or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("data має бути списком чисел.")

    plt.figure(figsize=(4, 4))
    plt.plot(data, marker='o', linestyle='-', color='blue')
    plt.title(title)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close()
    return buf
