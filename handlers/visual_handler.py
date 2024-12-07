from aiogram import Router, types
from utils.visual_utils import (
    generate_matplotlib_bar_chart,
    generate_seaborn_scatter_plot,
    generate_plotly_pie_chart,
    format_table_with_rich
)
import seaborn as sns

router = Router()

@router.message(commands=["plot"])
async def cmd_plot(message: types.Message):
    # Генерація Matplotlib графіка
    matches = ['Мач 1', 'Мач 2', 'Мач 3', 'Мач 4', 'Мач 5']
    wins = [1, 0, 1, 1, 0]
    buf_matplotlib = generate_matplotlib_bar_chart(matches, wins)
    await message.answer_photo(photo=buf_matplotlib, caption="📊 Статистика Перемог")

    # Генерація Seaborn графіка
    data = sns.load_dataset("tips")
    buf_seaborn = generate_seaborn_scatter_plot(data)
    await message.answer_photo(photo=buf_seaborn, caption="📉 Відношення Чеку до Чаю")

    # Генерація Plotly графіка
    labels = ['Атака', 'Захист', 'Магія', 'Лікування']
    values = [55, 20, 15, 10]
    buf_plotly = generate_plotly_pie_chart(labels, values)
    await message.answer_photo(photo=buf_plotly, caption="📈 Розподіл Навичок")

@router.message(commands=["table"])
async def cmd_table(message: types.Message):
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
