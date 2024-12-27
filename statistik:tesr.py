from aiogram import Router, Bot, F
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StatisticsCommand:
    """Клас для обробки команди статистики"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.router = Router()
        self._setup_handlers()
    
    async def setup_bot_commands(self):
        """Налаштування команд бота"""
        commands = [
            BotCommand(
                command="statistics",
                description="📊 Переглянути вашу статистику"
            )
        ]
        
        try:
            await self.bot.set_my_commands(
                commands=commands,
                scope=BotCommandScopeDefault()
            )
            logger.info("Bot commands have been set up successfully")
        except Exception as e:
            logger.error(f"Error setting up bot commands: {e}")

    def _setup_handlers(self):
        """Налаштування обробників команд"""
        self.router.message.register(
            self.show_statistics,
            Command("statistics")
        )

    async def get_user_statistics(self, user_id: int) -> dict:
        """
        Отримання статистики користувача
        В майбутньому тут буде звернення до бази даних
        """
        # TODO: Implement database integration
        return {
            "username": "is_mlbb",
            "level": 1,
            "rating": 0.0,
            "tasks": 0,
            "missions": 0,
            "quizzes": 0,
            "screenshots": 0,
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "tournaments": 0,
            "badges": 0,
            "last_updated": datetime.utcnow()
        }

    def format_statistics(self, stats: dict) -> str:
        """Форматування статистики для відображення"""
        return f"""🌟 Епічний профіль гравця 🌟

👤 Ім'я: {stats['username']}
🎯 Рівень: {stats['level']}
🌟 Рейтинг: {stats['rating']}

🏆 ДОСЯГНЕННЯ
📌 Завдань: {stats['tasks']}
🎮 Місій: {stats['missions']}
🧠 Вікторин: {stats['quizzes']}
🖼️ Скріншотів: {stats['screenshots']}

⚔️ МАТЧІ
🏟️ Матчів: {stats['matches']}
🏅 Виграші: {stats['wins']}
❌ Поразки: {stats['losses']}

🏅 ТУРНІРИ
📅 Участь: {stats['tournaments']}
🏵️ Бейджів: {stats['badges']}
🔄 Останнє оновлення: {stats['last_updated'].strftime('%d.%m.%Y %H:%M')}

🤖 Готові підкорювати нові вершини у Mobile Legends?
⚔️ Вибирайте свій шлях і ставайте ще сильнішими! Разом до перемоги!"""

    async def show_statistics(self, message: Message):
        """Обробник команди /statistics"""
        try:
            # Отримуємо статистику користувача
            stats = await self.get_user_statistics(message.from_user.id)
            
            # Форматуємо та відправляємо повідомлення
            await message.answer(
                text=self.format_statistics(stats),
                parse_mode="HTML"
            )
            logger.info(f"Statistics shown for user {message.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error showing statistics: {e}")
            await message.answer(
                "⚠️ Виникла помилка при завантаженні статистики. "
                "Спробуйте пізніше або зверніться до адміністратора."
            )

# Функція для налаштування команди статистики
async def setup_statistics_command(bot: Bot) -> Router:
    """Налаштування команди статистики"""
    statistics_command = StatisticsCommand(bot)
    await statistics_command.setup_bot_commands()
    return statistics_command.router

# Приклад використання у основному файлі бота:
'''
async def main():
    bot = Bot(token="YOUR_BOT_TOKEN")
    dp = Dispatcher()
    
    # Налаштування команди статистики
    statistics_router = await setup_statistics_command(bot)
    dp.include_router(statistics_router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''
