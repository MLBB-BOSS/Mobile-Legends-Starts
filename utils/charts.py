from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command
import io
import matplotlib.pyplot as plt

router = Router()

def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    plt.figure(figsize=(4,4))
    plt.plot(rating_history, marker='o')
    plt.title("Графік зміни рейтингу")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@router.message(Command("my_progress"))
async def show_progress(message: Message):
    rating_history = [100, 200, 250, 300]
    chart = generate_rating_chart(rating_history)
    photo_file = InputFile(chart, filename="chart.png")
    await message.answer_photo(photo=photo_file, caption="Ваш прогрес за останні сеанси")
