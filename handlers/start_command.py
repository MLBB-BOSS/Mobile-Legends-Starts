from aiogram import Router, types
from aiogram.filters import CommandStart
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_command(message: types.Message):
    user_name = message.from_user.first_name

    welcome_text = f'''
🎮 *Вітаю, {user_name}!* 🎮

🌟 Я твій особистий помічник у світі Mobile Legends: Bang Bang! 🌟

Ось що я можу для тебе зробити:
• 📱 Показати інформацію про героїв
• 🛡️ Розповісти про мета-picks
• 🗺️ Дати поради по стратегії
• 💪 Допомогти з білдами

*Основні команди:*
📍 /hero - список всіх героїв
📍 /meta - актуальний мета-звіт
📍 /build - гайди по білдам
📍 /help - додаткова допомога

_Готовий допомогти тобі стати кращим гравцем!_ 💪
'''

    try:
        await message.answer(text=welcome_text, parse_mode="Markdown")
        logger.info(f"Відправлено привітання користувачу {user_name} (ID: {message.from_user.id})")
    except Exception as e:
        logger.error(f"Помилка при відправці привітання: {e}")
        await message.answer("Вітаю! Я бот Mobile Legends. Використовуйте /help для перегляду команд.")
