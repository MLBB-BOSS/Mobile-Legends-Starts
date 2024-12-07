# handlers/visual_handler.py

from aiogram import Router, types
from utils.visual_utils import (
    generate_matplotlib_bar_chart,
    generate_seaborn_scatter_plot,
    generate_plotly_pie_chart,
    format_table_with_rich
)
import seaborn as sns
from aiogram.types import InputFile  # Додайте цей імпорт, якщо ще не додано

router = Router()

@router.message(commands=["plot"])
async def cmd_plot(message: types.Message):
    """
    Обробник команди /plot.
    Генерує графіки та відправляє їх користувачу.
    """
    # Генерація Matplotlib графіка
    categories = ['Перемоги', 'Поразки', 'Нічі']
    values = [15, 5, 2]
    title = "Ваші Ігрові Статистики"
    buf_matplotlib = generate_matplotlib_bar_chart(categories, values, title=title)
    await message.answer_photo(photo=InputFile(buf_matplotlib, filename="stats.png"), caption="📊 Статистика Перемог")

    # Генерація Seaborn графіка
    data = sns.load_dataset("tips")
    buf_seaborn = generate_seaborn_scatter_plot(data, x='total_bill', y='tip', hue='day', title="Відношення Чеку до Чаю")
    await message.answer_photo(photo=InputFile(buf_seaborn, filename="scatter.png"), caption="📉 Відношення Чеку до Чаю")

    # Генерація Plotly графіка
    labels = ['Атака', 'Захист', 'Магія', 'Лікування']
    values_plotly = [55, 20, 15, 10]
    buf_plotly = generate_plotly_pie_chart(labels, values_plotly, title="Розподіл Навичок")
    await message.answer_photo(photo=InputFile(buf_plotly, filename="pie_chart.png"), caption="📈 Розподіл Навичок")

@router.message(commands=["table"])
async def cmd_table(message: types.Message):
    """
    Обробник команди /table.
    Генерує таблицю та відправляє її користувачу.
    """
    # Дані для таблиці
    data = [
        ["Мач 1", "Перемога"],
        ["Мач 2", "Поразка"],
        ["Мач 3", "Перемога"],
        ["Мач 4", "Перемога"],
        ["Мач 5", "Поразка"]
    ]
    headers = ["Матч", "Результат"]
    
    # Форматування таблиці з використанням Rich
    formatted_table = format_table_with_rich(data, headers)
    await message.answer(f"📋 <b>Таблиця Результатів:</b>\n<code>{formatted_table}</code>", parse_mode='HTML')
