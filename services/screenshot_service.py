from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from models.screenshot import Screenshot, User
from database.repositories.screenshot_repository import ScreenshotRepository
from database.repositories.user_repository import UserRepository

class ScreenshotService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.screenshot_repo = ScreenshotRepository(session)
        self.user_repo = UserRepository(session)

    async def save_hero_screenshot(
        self,
        telegram_id: int,
        file_id: str,
        hero_name: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> Screenshot:
        """
        Зберігає скріншот героя з додатковими метаданими
        
        Args:
            telegram_id: ID користувача в Telegram
            file_id: ID файлу в Telegram
            hero_name: Ім'я героя (опціонально)
            metadata: Додаткові дані про скріншот (опціонально)
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        
        return await self.screenshot_repo.add_screenshot(
            user_id=user.id,
            file_id=file_id,
            hero_name=hero_name,
            metadata=metadata
        )

    async def get_user_screenshots(
        self,
        telegram_id: int,
        limit: int = 10
    ) -> List[Screenshot]:
        """
        Отримує останні скріншоти користувача
        
        Args:
            telegram_id: ID користувача в Telegram
            limit: Кількість скріншотів для повернення
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return []
        
        return await self.screenshot_repo.get_user_screenshots(
            user_id=user.id,
            limit=limit
        )

    async def get_hero_screenshots(
        self,
        hero_name: str,
        limit: int = 10
    ) -> List[Screenshot]:
        """
        Отримує скріншоти конкретного героя
        
        Args:
            hero_name: Ім'я героя
            limit: Кількість скріншотів для повернення
        """
        return await self.screenshot_repo.get_hero_screenshots(
            hero_name=hero_name,
            limit=limit
        )

    async def delete_screenshot(
        self,
        screenshot_id: int,
        telegram_id: int
    ) -> bool:
        """
        Видаляє скріншот, перевіряючи права доступу
        
        Args:
            screenshot_id: ID скріншота
            telegram_id: ID користувача в Telegram для перевірки прав
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        
        screenshot = await self.screenshot_repo.get_by_id(screenshot_id)
        if not screenshot or screenshot.user_id != user.id:
            return False
        
        return await self.screenshot_repo.delete_screenshot(screenshot_id)

    @staticmethod
    def format_screenshot_info(screenshot: Screenshot) -> str:
        """
        Форматує інформацію про скріншот для відображення
        
        Args:
            screenshot: Об'єкт скріншота
        """
        info = [
            f"📸 Скріншот #{screenshot.id}",
            f"📅 Дата: {screenshot.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        if screenshot.hero_name:
            info.append(f"🦸 Герой: {screenshot.hero_name}")
        
        if screenshot.metadata:
            info.append("\n📝 Додаткова інформація:")
            for key, value in screenshot.metadata.items():
                info.append(f"- {key}: {value}")
        
        return "\n".join(info)

    @staticmethod
    def validate_screenshot_metadata(metadata: dict) -> bool:
        """
        Перевіряє метадані скріншота на коректність
        
        Args:
            metadata: Словник з метаданими
        """
        required_fields = ["game_mode", "result"]
        return all(field in metadata for field in required_fields)
