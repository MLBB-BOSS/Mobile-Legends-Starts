import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import io
from telegram import InputFile
from rich.console import Console
from rich.table import Table

# Ініціалізація Rich для форматування тексту
console = Console(record=True)

def generate_matplotlib_bar_chart(matches, wins) -> io.BytesIO:
    plt.figure(figsize=(6,4))
    plt.bar(matches, wins, color='skyblue')
    plt.xlabel('Матчі')
    plt.ylabel('Перемоги')
    plt.title('Статистика Перемог')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def generate_seaborn_scatter_plot(data) -> io.BytesIO:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x='total_bill', y='tip', hue='day', data=data)
    plt.title('Відношення Чеку до Чаю')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def generate_plotly_pie_chart(labels, values) -> io.BytesIO:
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='Розподіл Навичок')
    
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
