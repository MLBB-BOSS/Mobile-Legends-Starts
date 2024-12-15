import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO

def generate_rating_chart(rating_history: list) -> BytesIO:
    """
    Генерує графік рейтингу користувача у кіберспортивному стилі.

    Args:
        rating_history (list): Список значень рейтингу для графіку.

    Returns:
        BytesIO: Графік у вигляді байтового потоку.
    """
    # Встановлення стилю графіку
    plt.style.use('dark_background')  # Темний фон

    # Створення фігури
    fig, ax = plt.subplots(figsize=(8, 5))  # Розмір графіку

    # Основна лінія графіку
    ax.plot(
        rating_history, 
        marker='o', 
        linestyle='-', 
        linewidth=2.5, 
        color='#00FFEA',  # Бірюзова лінія
        markerfacecolor='#FF5733',  # Помаранчеві маркери
        markeredgecolor='#FFD700',  # Золота обводка маркерів
        markersize=10
    )

    # Додаткові стилі осей
    ax.set_facecolor('#111111')  # Темний сірий фон для області графіку
    ax.grid(color='#333333', linestyle='--', linewidth=0.5)  # Сітка
    ax.tick_params(axis='both', colors='white')  # Колір підписів осей

    # Заголовок та осі
    ax.set_title("Ігрова статистика рейтингу", fontsize=16, fontweight='bold', color='#FF5733')
    ax.set_xlabel("Період", fontsize=12, color='#00FFEA')
    ax.set_ylabel("Рейтинг", fontsize=12, color='#00FFEA')

    # Ефект рамки
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, edgecolor='#FF5733', fill=False, lw=2))

    # Збереження у байтовий потік
    chart_io = BytesIO()
    plt.tight_layout()
    plt.savefig(chart_io, format='png', dpi=300)
    plt.close(fig)

    return chart_io
