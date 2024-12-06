from aiogram import Dispatcher, types
from aiogram.filters import F

# Приклад функції для обробки кнопки Start
async def cmd_start(message: types.Message):
    await message.answer("Вітаємо у боті! Оберіть один з варіантів меню.")

# Функція реєстрації обробників
def register_navigation_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, F.text == "Start")
    # Додайте інші обробники тут
