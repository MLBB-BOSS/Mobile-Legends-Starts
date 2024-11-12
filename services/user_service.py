# services/user_service.py
import logging
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import joinedload

from models.user import User
from models.hero import Hero
from models.hero_media import HeroMedia
from services.base_service import BaseService

logger = logging.getLogger(__name__)

class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_user(self, telegram_id: int, username: str) -> Optional[User]:
        """
        Створення або отримання існуючого користувача
        
        Args:
            telegram_id: Telegram ID користувача
            username: Ім'я користувача в Telegram
        """
        try:
            # Перевірка чи користувач вже існує
            query = select(User).where(User.telegram_id == telegram_id)
            result = await self._session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                # Оновлюємо username якщо змінився
                if user.username != username:
                    user.username = username
                    await self.commit()
                return user
            
            # Створюємо нового користувача
            user = User(
                telegram_id=telegram_id,
                username=username,
                created_at=datetime.utcnow()
            )
            self._session.add(user)
            await self.commit()
            logger.info(f"Created new user: {username}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    async def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """
        Отримання профілю користувача з статистикою
        
        Args:
            user_id: ID користувача
        """
        try:
            # Отримуємо користувача з його досягненнями
            query = select(User).where(User.id == user_id).options(
                joinedload(User.achievements)
            )
            result = await self._session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return None

            # Підраховуємо статистику
            heroes_query = select(func.count(Hero.id)).where(
                Hero.contributor_id == user_id,
                Hero.status == 'approved'
            )
            heroes_result = await self._session.execute(heroes_query)
            approved_heroes = heroes_result.scalar_one()

            media_query = select(func.count(HeroMedia.id)).where(
                HeroMedia.contributor_id == user_id
            )
            media_result = await self._session.execute(media_query)
            total_media = media_result.scalar_one()

            votes_query = select(func.sum(HeroMedia.votes)).where(
                HeroMedia.contributor_id == user_id
            )
            votes_result = await self._session.execute(votes_query)
            total_votes = votes_result.scalar_one() or 0

            return {
                'id': user.id,
                'username': user.username,
                'points': user.points,
                'rank': await self._calculate_user_rank(user.points),
                'statistics': {
                    'approved_heroes': approved_heroes,
                    'total_media': total_media,
                    'total_votes': total_votes,
                    'contribution_count': user.contribution_count
                },
                'achievements': [
                    {
                        'id': achievement.id,
                        'name': achievement.name,
                        'description': achievement.description,
                        'earned_at': achievement.earned_at
                    } for achievement in user.achievements
                ],
                'created_at': user.created_at
            }

        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None

    async def update_user_points(self, user_id: int, points: int) -> bool:
        """
        Оновлення балів користувача
        
        Args:
            user_id: ID користувача
            points: Кількість балів для додавання (може бути від'ємною)
        """
        try:
            query = update(User).where(User.id == user_id).values(
                points=User.points + points,
                contribution_count=User.contribution_count + 1
            )
            await self._session.execute(query)
            await self.commit()
            logger.info(f"Updated points for user {user_id}: {points}")
            return True
        except Exception as e:
            logger.error(f"Error updating user points: {e}")
            return False

    async def get_top_contributors(self, limit: int = 10) -> List[Dict]:
        """
        Отримання топ користувачів за внеском
        
        Args:
            limit: Кількість користувачів у списку
        """
        try:
            query = select(User).order_by(
                User.points.desc()
            ).limit(limit)
            
            result = await self._session.execute(query)
            users = result.scalars().all()

            return [{
                'id': user.id,
                'username': user.username,
                'points': user.points,
                'rank': await self._calculate_user_rank(user.points),
                'contribution_count': user.contribution_count
            } for user in users]

        except Exception as e:
            logger.error(f"Error getting top contributors: {e}")
            return []

    async def _calculate_user_rank(self, points: int) -> str:
        """
        Розрахунок рангу користувача на основі балів
        
        Args:
            points: Кількість балів користувача
        """
        if points >= 1000:
            return "Mythical Glory"
        elif points >= 750:
            return "Mythic"
        elif points >= 500:
            return "Legend"
        elif points >= 250:
            return "Epic"
        elif points >= 100:
            return "Grandmaster"
        elif points >= 50:
            return "Master"
        else:
            return "Elite"

    async def check_user_ban(self, user_id: int) -> bool:
        """
        Перевірка чи користувач заблокований
        
        Args:
            user_id: ID користувача
        """
        try:
            query = select(User.is_banned, User.ban_reason).where(User.id == user_id)
            result = await self._session.execute(query)
            is_banned, ban_reason = result.one_or_none()
            return is_banned
        except Exception as e:
            logger.error(f"Error checking user ban: {e}")
            return False
