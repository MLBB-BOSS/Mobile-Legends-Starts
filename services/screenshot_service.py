from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from models.screenshot import Screenshot, User
from database.repositories.screenshot_repository import ScreenshotRepository
from database.repositories.user_repository import UserRepository
from services.exceptions import (
    ValidationError,
    ScreenshotError,
    UserNotFoundError,
    PermissionError
)

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
            
        Raises:
            ValidationError: Якщо дані некоректні
            UserNotFoundError: Якщо користувача не знайдено
            ScreenshotError: При помилці збереження скріншота
        """
        try:
            if not file_id:
                raise ValidationError("ID файлу не може бути порожнім")
            
            user = await self.user_repo.get_by_telegram_id(telegram_id)
            if not user:
                raise UserNotFoundError(telegram_id)
            
            # Валідація метаданих
            if metadata and not self.validate_screenshot_metadata(metadata):
                raise ValidationError("Некоректні метадані скріншота")
            
            return await self.screenshot_repo.add_screenshot(
                user_id=user.id,
                file_id=file_id,
                hero_name=hero_name,
                metadata=metadata
            )
            
        except (ValidationError, UserNotFoundError):
            raise
        except Exception as e:
            raise ScreenshotError(f"Помилка при збереженні скріншота: {str(e)}")

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
            
        Raises:
            UserNotFoundError: Якщо користувача не знайдено
        """
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundError(telegram_id)
        
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
            
        Raises:
            ValidationError: Якщо ім'я героя порожнє
        """
        if not hero_name:
            raise ValidationError("Ім'я героя не може бути порожнім")
            
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
            
        Raises:
            UserNotFoundError: Якщо користувача не знайдено
            ScreenshotError: Якщо скріншот не знайдено
            PermissionError: Якщо користувач не має прав на видалення
        """
        try:
            user = await self.user_repo.get_by_telegram_id(telegram_id)
            if not user:
                raise UserNotFoundError(telegram_id)
            
            screenshot = await self.screenshot_repo.get_by_id(screenshot_id)
            if not screenshot:
                raise ScreenshotError("Скріншот не знайдено")
            
            if screenshot.user_id != user.id:
                raise PermissionError("Ви не можете видалити чужий скріншот")
            
            return await self.screenshot_repo.delete_screenshot(screenshot_id)
            
        except (UserNotFoundError, ScreenshotError, PermissionError):
            raise
        except Exception as e:
            raise ScreenshotError(f"Помилка при видаленні скріншота: {str(e)}")

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
        if not isinstance(metadata, dict):
            return False
            
        required_fields = ["game_mode", "result"]
        return all(field in metadata for field in required_fields)
