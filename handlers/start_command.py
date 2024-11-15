from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

# Створюємо роутер для повідомлень
router = Router(name="message_router")

# Обробка текстових повідомлень
@router.message(F.text)
async def handle_text_message(message: Message):
    try:
        text = message.text.lower()
        
        # Базова обробка повідомлень
        if "привіт" in text:
            await message.answer("Привіт! Чим можу допомогти?")
        
        elif "допомога" in text:
            await message.answer(
                "Ось список доступних команд:\n"
                "/start - Почати роботу з ботом\n"
                "/hero - Переглянути героїв\n"
                "/help - Отримати допомогу"
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

# Обробка команди /help
@router.message(Command("help"))
async def help_command(message: Message):
    try:
        help_text = (
            "🤖 *Допомога по використанню бота*\n\n"
            "*Основні команди:*\n"
            "• /start - Почати роботу з ботом\n"
            "• /hero - Переглянути список героїв\n"
            "• /help - Показати це повідомлення\n\n"
            "*Додаткові функції:*\n"
            "• Виберіть клас героя за допомогою кнопок\n"
            "• Перегляньте інформацію про конкретного героя\n"
            "• Використовуйте кнопку 'Назад' для повернення до меню\n\n"
            "Якщо у вас виникли проблеми, спробуйте перезапустити бота командою /start"
        )
        
        await message.answer(help_text, parse_mode="Markdown")
        logger.info(f"Відправлено довідку користувачу {message.from_user.id}")
    
    except Exception as e:
        logger.error(f"Помилка при відправці довідки: {e}")
        await message.answer("Вибачте, сталася помилка при відображенні довідки.")

# Обробка невідомих команд
@router.message(Command(""))
async def unknown_command(message: Message):
    await message.answer(
        "Невідома команда. Використайте /help для перегляду доступних команд."
    )
    logger.warning(f"Користувач {message.from_user.id} використав невідому команду: {message.text}")
