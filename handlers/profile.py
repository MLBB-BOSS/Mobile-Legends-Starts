# handlers/profile.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.exceptions import TelegramAPIError
from logging import getLogger
from io import BytesIO

from utils.db import get_db_session
from services.user_service import UserService
from services.chart_service import ChartService
from exceptions import UserNotFoundError, ChartGenerationError

logger = getLogger(__name__)

class DbSessionMiddleware:
    """Middleware for managing database sessions"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with get_db_session() as session:
            data["db"] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error in handler: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()

class ProfileHandler:
    """Handler for profile-related commands"""
    
    def __init__(self):
        self.router = Router(name="profile")
        self.router.message.middleware(DbSessionMiddleware())
        self._setup_handlers()
        self.logger = getLogger(__name__)

    def _setup_handlers(self) -> None:
        """Setup message handlers"""
        self.router.message.register(
            self.show_profile,
            Command("profile")
        )

    async def _generate_profile_chart(
        self,
        user_id: int,
        chart_service: ChartService
    ) -> BufferedInputFile:
        """
        Generate profile chart
        
        Args:
            user_id: User ID
            chart_service: Chart service instance
            
        Returns:
            BufferedInputFile: Chart image ready to send
            
        Raises:
            ChartGenerationError: If chart generation fails
        """
        try:
            chart_bytes = await chart_service.generate_rating_chart(user_id)
            chart_bytes.seek(0)
            
            return BufferedInputFile(
                chart_bytes.read(),
                filename=f'rating_chart_{user_id}.png'
            )
        except Exception as e:
            raise ChartGenerationError(f"Failed to generate chart: {e}")

    async def show_profile(
        self,
        message: Message,
        db: AsyncSession
    ) -> None:
        """
        Handle /profile command
        
        Args:
            message: Telegram message
            db: Database session
        """
        try:
            user_id = message.from_user.id
            
            # Initialize services
            user_service = UserService(db)
            chart_service = ChartService(db)
            
            # Get user profile data
            try:
                profile_text = await user_service.get_profile_text(user_id)
            except UserNotFoundError:
                await message.answer(
                    "⚠️ Профіль не знайдено. Використайте /start для реєстрації."
                )
                return
                
            # Generate chart
            try:
                chart_file = await self._generate_profile_chart(
                    user_id,
                    chart_service
                )
            except ChartGenerationError as e:
                self.logger.error(f"Chart generation error: {e}")
                await message.answer(
                    f"{profile_text}\n\n⚠️ Не вдалося згенерувати графік."
                )
                return

            # Send profile with chart
            try:
                await message.answer_photo(
                    photo=chart_file,
                    caption=profile_text,
                    parse_mode="HTML"
                )
            except TelegramAPIError as e:
                self.logger.error(f"Failed to send profile: {e}")
                await message.answer(
                    "❌ Помилка при відправці профілю. Спробуйте пізніше."
                )

        except Exception as e:
            self.logger.error(f"Unexpected error in show_profile: {e}")
            await message.answer(
                "❌ Сталася несподівана помилка. Спробуйте пізніше."
            )

# Create handler instance
profile_handler = ProfileHandler()
# Export router
profile_router = profile_handler.router
