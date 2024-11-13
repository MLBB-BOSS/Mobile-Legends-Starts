from models.screenshot import Screenshot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ScreenshotService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_screenshot(self, user_id: int, file_id: str, file_unique_id: str, 
                              width: int, height: int, file_path: str) -> Screenshot:
        screenshot = Screenshot(
            user_id=user_id,
            file_id=file_id,
            file_unique_id=file_unique_id,
            width=width,
            height=height,
            file_path=file_path
        )
        self.session.add(screenshot)
        await self.session.commit()
        await self.session.refresh(screenshot)
        return screenshot

    async def get_user_screenshots(self, user_id: int) -> list[Screenshot]:
        result = await self.session.execute(
            select(Screenshot)
            .where(Screenshot.user_id == user_id)
            .order_by(Screenshot.created_at.desc())
        )
        return result.scalars().all()

    async def get_screenshot_by_file_id(self, file_unique_id: str) -> Screenshot:
        result = await self.session.execute(
            select(Screenshot)
            .where(Screenshot.file_unique_id == file_unique_id)
        )
        return result.scalar_one_or_none()
