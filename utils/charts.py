import io
import matplotlib.pyplot as plt

from aiogram import Router

charts_router = Router()

# Додаткові хендлери для роботи з графіками
@charts_router.message(Command("chart"))
async def send_chart(message: Message):
    # Логіка для відправки графіка
    pass

def create_chart(data: list[int], title: str = "Default Title") -> io.BytesIO:
    """
    Створює простий графік на основі переданих даних.
    """
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
