import matplotlib.pyplot as plt
from io import BytesIO

def generate_rating_chart(rating_history: list) -> BytesIO:
    """
    Генерує графік рейтингу користувача.

    Args:
        rating_history (list): Список значень рейтингу для графіку.

    Returns:
        BytesIO: Графік у вигляді байтового потоку.
    """
    # Налаштування графіку
    plt.figure(figsize=(8, 4))
    plt.plot(rating_history, marker='o', linestyle='-', linewidth=2)
    plt.title("Ріст рейтингу користувача")
    plt.xlabel("Період")
    plt.ylabel("Рейтинг")
    plt.grid(True)
    plt.tight_layout()

    # Збереження у BytesIO
    chart_io = BytesIO()
    plt.savefig(chart_io, format='png')
    plt.close()

    return chart_io
