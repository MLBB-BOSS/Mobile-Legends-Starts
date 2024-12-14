# utils/charts.py
import io
import matplotlib.pyplot as plt
import logging

def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    """
    Генерує графік зміни рейтингу.
    rating_history - список рейтингів по часу, наприклад: [100, 200, 250, 300].
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("Генерація графіка рейтингу")

        plt.figure(figsize=(6, 4))
        plt.plot(rating_history, marker='o', linestyle='-', color='b')
        plt.title("Графік зміни рейтингу")
        plt.xlabel("Сеанс")
        plt.ylabel("Рейтинг")
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        logger.info("Графік рейтингу успішно згенеровано")
        return buf
    except Exception as e:
        logger.error(f"Сталася помилка при генерації графіка: {e}")
        raise