from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import logging

logger = logging.getLogger(__name__)
router = Router(name="message_router")

@router.message(F.text)
async def handle_text_message(message: Message):
    try:
        text = message.text.lower()

        if "привіт" in text:
            await message.answer("Привіт! Чим можу допомогти?")
        elif "допомога" in text:
            await message.answer(
                "Ось список доступних команд:\n"
                "/start - Почати роботу з ботом\n"
                "/hero - Переглянути героїв\n/help - Отримати допомогу"
            )
        else:
            await message.answer(
                "Я не впевнений, що розумію. Спробуйте використати команди:\n"
                "/start - для початку роботи\n"
                "/hero - для перегляду героїв"
            )

        logger.info(f"Оброблено повідомлення від користувача {message.from_user.id}: {text}")
    except Exception as e:
        logger.error(f"Помилка при обробці повідомлення: {e}")
        await message.answer("Вибачте, сталася помилка при обробці вашого повідомлення.")
