import io
import matplotlib.pyplot as plt

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
    plt.close()  # очищаємо, щоб уникнути витоків пам'яті
    return buf
