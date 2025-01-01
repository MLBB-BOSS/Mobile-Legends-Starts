# services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from exceptions import UserNotFoundError

class UserService:
    """Service for user-related operations"""
    
    def __init__(self, db: AsyncSession):
        self._db = db
        self.logger = getLogger(__name__)

    async def get_profile_text(self, user_id: int) -> str:
        """
        Get formatted profile text
        
        Args:
            user_id: User ID
            
        Returns:
            str: Formatted profile text
            
        Raises:
            UserNotFoundError: If user not found
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await self._db.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                raise UserNotFoundError(f"User {user_id} not found")
            
            return (
                f"👤 <b>Профіль користувача</b>\n\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"📝 Нік: <code>{user.username}</code>\n"
                f"📈 Рейтинг: <code>{user.rating}</code>\n"
                f"🏆 Перемог: <code>{user.wins}</code>\n"
                f"💪 Вінрейт: <code>{user.winrate:.1f}%</code>"
            )
            
        except Exception as e:
            self.logger.error(f"Error getting profile text: {e}")
            raise

# services/chart_service.py
class ChartService:
    """Service for chart generation"""
    
    def __init__(self, db: AsyncSession):
        self._db = db
        self.logger = getLogger(__name__)

    async def generate_rating_chart(self, user_id: int) -> BytesIO:
        """
        Generate rating chart
        
        Args:
            user_id: User ID
            
        Returns:
            BytesIO: Chart image bytes
            
        Raises:
            ChartGenerationError: If generation fails
        """
        try:
            # Get rating history
            query = select(UserRating).where(
                UserRating.user_id == user_id
            ).order_by(UserRating.timestamp)
            
            result = await self._db.execute(query)
            ratings = [r.rating for r in result.scalars()]
            
            # Generate chart
            buffer = BytesIO()
            plt.figure(figsize=(10, 6))
            plt.plot(ratings, marker='o')
            plt.title("Історія рейтингу")
            plt.grid(True)
            
            plt.savefig(buffer, format='png')
            plt.close()
            
            return buffer
            
        except Exception as e:
            raise ChartGenerationError(f"Failed to generate chart: {e}")
