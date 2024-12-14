from aiogram.types import InputFile
from utils.charts import generate_rating_chart

rating_history = [100, 200, 250, 300]
chart = generate_rating_chart(rating_history)
photo_file = InputFile(chart, filename="chart.png")

await message.answer_photo(photo=photo_file, caption="Ваш прогрес за останні сеанси")
