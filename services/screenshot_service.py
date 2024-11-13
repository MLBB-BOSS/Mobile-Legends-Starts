from models.screenshot import Screenshot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

class ScreenshotService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_screenshot(self, user_id: int, file_id: str, hero_name: Optional[str] = None) -> Screenshot:
        """Зберігає новий скріншот"""
        screenshot = Screenshot(
            user_id=user_id,
            file_id=file_id,
            hero_name=hero_name
        )
        self.session.add(screenshot)
        await self.session.commit()
        return screenshot

    async def get_user_screenshots(self, user_id: int) -> List[Screenshot]:
        """Отримує всі скріншоти користувача"""
        query = select(Screenshot).where(Screenshot.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_screenshot(self, screenshot_id: int) -> Optional[Screenshot]:
        """Отримує конкретний скріншот за ID"""
        query = select(Screenshot).where(Screenshot.id == screenshot_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
