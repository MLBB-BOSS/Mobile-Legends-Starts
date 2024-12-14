# utils/charts.py
import io
import matplotlib.pyplot as plt
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    try:
        logger.info("Генерація графіка рейтингу")
        plt.switch_backend('Agg')  # Безвіджетний бекенд для серверних середовищ

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