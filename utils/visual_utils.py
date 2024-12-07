# utils/visual_utils.py

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import io
from aiogram.types import InputFile  # Виправлений імпорт
from rich.console import Console
from rich.table import Table

# Ініціалізація Rich для форматування тексту
console = Console()

def generate_matplotlib_bar_chart(categories, values, title="Статистика"):
    """
    Генерує бар-чарт за допомогою Matplotlib та повертає його у вигляді буфера байтів.

    :param categories: Список категорій (наприклад, назви матчів)
    :param values: Список значень для кожної категорії (наприклад, кількість перемог)
    :param title: Заголовок графіка
    :return: Буфер байтів з збереженим графіком
    """
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, values, color='skyblue')
    plt.xlabel('Категорії')
    plt.ylabel('Значення')
    plt.title(title)
    plt.tight_layout()

    # Додавання значень зверху кожного бару
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, yval, ha='center', va='bottom')

    # Збереження графіка у буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def generate_seaborn_scatter_plot(data, x='total_bill', y='tip', hue=None, title="Статистика"):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x=x, y=y, hue=hue)
    plt.title(title)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def generate_plotly_pie_chart(labels, values, title="Розподіл Навичок"):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=title)

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    return buf

def format_table_with_rich(data: list, headers: list) -> str:
    table = Table(show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    
    for row in data:
        table.add_row(*[str(item) for item in row])
    
    # Render table to string
    console.print(table)
    return console.export_text()
