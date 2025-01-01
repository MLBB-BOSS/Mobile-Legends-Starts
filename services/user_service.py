# services/user_service.py
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User

class UserService:
    """Async user data service"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._collection = db.users
        self.logger = getLogger(__name__)

    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            data = await self._collection.find_one({"_id": user_id})
            return User(**data) if data else None
        except Exception as e:
            self.logger.error(f"Error getting user {user_id}: {e}")
            raise

    async def update_user(self, user_id: int, update: Dict[str, Any]) -> None:
        """Update user data"""
        try:
            await self._collection.update_one(
                {"_id": user_id},
                {"$set": update},
                upsert=True
            )
        except Exception as e:
            self.logger.error(f"Error updating user {user_id}: {e}")
            raise

# services/stats_service.py
class StatsService:
    """Async statistics service"""
    
    def __init__(self, db: AsyncIOMotorDatabase, http: aiohttp.ClientSession):
        self._db = db
        self._http = http
        self._collection = db.stats
        self.logger = getLogger(__name__)

    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            # Get local stats
            local_stats = await self._collection.find_one({"user_id": user_id})
            
            # Get remote stats
            async with self._http.get(f"/api/stats/{user_id}") as response:
                remote_stats = await response.json()
            
            # Combine stats
            return {**local_stats, **remote_stats} if local_stats else remote_stats
            
        except Exception as e:
            self.logger.error(f"Error getting stats for user {user_id}: {e}")
            raise
