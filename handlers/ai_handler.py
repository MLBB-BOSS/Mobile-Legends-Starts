# handlers/ai_handler.py

from aiogram.types import ChatType

ALLOWED_USERS = {123456789, 987654321}  # Замість цих чисел використовуйте ID дозволених користувачів

@router.message(Command("ai"))
async def handle_openai_request(message: Message, state: FSMContext):
    if message.from_user.id not in ALLOWED_USERS:
        await message.answer("Вибачте, у вас немає доступу до цієї команди.")
        return

    user_prompt = message.text.partition(' ')[2].strip()  # Отримуємо текст після команди
    if not user_prompt:
        await message.answer("Введіть текст запиту після команди /ai.")
        return

    await message.answer("Запит обробляється, зачекайте...")
    response = await ask_openai(user_prompt)  # Виклик функції OpenAI
    await message.answer(response)
