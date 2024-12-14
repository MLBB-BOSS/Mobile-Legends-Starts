import io
import matplotlib.pyplot as plt
from aiogram.types import Message, InputFile
from aiogram import Router

router = Router()

def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    """
    rating_history - список рейтингів по часу.
    Для прикладу: [100, 200, 250, 300]
    """
    plt.figure(figsize=(4,4))
    plt.plot(rating_history, marker='o')
    plt.title("Графік зміни рейтингу")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()  # Очищуємо щоб уникнути витоків пам'яті
    return buf

@router.message(commands=['my_progress'])
async def show_progress(message: Message):
    rating_history = [100, 200, 250, 300]
    chart = generate_rating_chart(rating_history)
    photo_file = InputFile(chart, filename="chart.png")
    await message.answer_photo(photo=photo_file, caption="Ваш прогрес за останні сеанси")
