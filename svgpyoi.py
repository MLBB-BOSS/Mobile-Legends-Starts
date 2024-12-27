import os
import cairosvg
from pathlib import Path
from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import logging

class ProfileImageGenerator:
    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = temp_dir
        self.logger = logging.getLogger(__name__)
        self._ensure_temp_dir()

    def _ensure_temp_dir(self):
        """Створення тимчасової директорії"""
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

    def _get_temp_path(self, filename: str) -> str:
        """Отримання шляху до тимчасового файлу"""
        return os.path.join(self.temp_dir, filename)

    async def generate_profile_image(self, user_data: dict) -> str:
        """
        Генерує зображення профілю на основі даних користувача
        
        Args:
            user_data (dict): Дані користувача для відображення в профілі
            
        Returns:
            str: Шлях до згенерованого зображення
        """
        # Читаємо шаблон SVG
        svg_template_path = "templates/profile_template.svg"
        with open(svg_template_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # Заміняємо плейсхолдери на реальні дані
        svg_content = svg_content.replace("Олег", user_data.get('username', 'Користувач'))
        svg_content = svg_content.replace("10", str(user_data.get('level', 1)))
        # Додайте інші заміни для інших даних...

        # Зберігаємо оновлений SVG
        temp_svg = self._get_temp_path(f"profile_{user_data['user_id']}.svg")
        with open(temp_svg, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        # Конвертуємо в PNG
        output_path = self._get_temp_path(f"profile_{user_data['user_id']}.png")
        try:
            cairosvg.svg2png(
                url=temp_svg,
                write_to=output_path,
                dpi=300,
                scale=2.0
            )
            return output_path
        except Exception as e:
            self.logger.error(f"Помилка при конвертації SVG в PNG: {e}")
            raise

class ProfileCommand:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.router = Router()
        self.image_generator = ProfileImageGenerator()
        self._setup_handlers()

    def _setup_handlers(self):
        """Налаштування обробників команд"""
        self.router.message.register(self.show_profile, Command("profile"))

    async def get_user_data(self, user_id: int) -> dict:
        """Отримання даних користувача"""
        # TODO: Реалізувати отримання даних з бази даних
        return {
            "user_id": user_id,
            "username": "is_mlbb",
            "level": 100,
            "rating": "ТОП 1",
            "badges": 56,
            "wins": 16,
            "activity_days": 15,
            "play_time": "40 годин",
            "friends": 5,
            "favorite_hero": "Ланселот",
            "last_tournament": "18.12.2024"
        }

    async def show_profile(self, message: Message):
        """Обробник команди /profile"""
        try:
            # Отримуємо дані користувача
            user_data = await self.get_user_data(message.from_user.id)
            
            # Генеруємо зображення профілю
            image_path = await self.image_generator.generate_profile_image(user_data)
            
            # Відправляємо зображення
            await message.answer_photo(
                photo=FSInputFile(image_path),
                caption=f"🎮 Профіль гравця {user_data['username']}"
            )
            
        except Exception as e:
            self.logger.error(f"Error showing profile: {e}")
            await message.answer("⚠️ Виникла помилка при генерації профілю")
        
        finally:
            # Видаляємо тимчасові файли
            try:
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                self.logger.error(f"Error cleaning up temporary files: {e}")

# Функція для налаштування команди профілю
async def setup_profile_command(bot: Bot) -> Router:
    """Налаштування команди профілю"""
    profile_command = ProfileCommand(bot)
    return profile_command.router

# Приклад використання у основному файлі бота:
'''
async def main():
    bot = Bot(token="YOUR_BOT_TOKEN")
    dp = Dispatcher()
    
    # Зберігаємо SVG шаблон
    os.makedirs("templates", exist_ok=True)
    with open("templates/profile_template.svg", "w", encoding="utf-8") as f:
        f.write(your_svg_template)
    
    # Налаштування команди профілю
    profile_router = await setup_profile_command(bot)
    dp.include_router(profile_router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''
