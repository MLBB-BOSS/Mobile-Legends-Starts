# services/achievement_service.py
import logging
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload

from models.achievement import Achievement
from models.user_achievement import UserAchievement
from models.user import User
from models.hero import Hero
from models.hero_media import HeroMedia
from services.base_service import BaseService

logger = logging.getLogger(__name__)

class AchievementService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def check_achievements(self, user_id: int) -> List[Achievement]:
        """
        Перевірка та нарахування нових досягнень для користувача
        
        Args:
            user_id: ID користувача
        Returns:
            Список нових досягнень
        """
        try:
            # Отримуємо всі досягнення користувача
            existing_achievements = await self.get_user_achievements(user_id)
            existing_ids = [a['id'] for a in existing_achievements]
            
            # Перевіряємо кожен тип досягнення
            new_achievements = []
            
            # Перевірка досягнень за кількістю героїв
            heroes_count = await self._count_user_heroes(user_id)
            hero_achievements = await self._check_hero_achievements(user_id, heroes_count, existing_ids)
            new_achievements.extend(hero_achievements)
            
            # Перевірка досягнень за кількістю голосів
            votes_count = await self._count_user_votes(user_id)
            vote_achievements = await self._check_vote_achievements(user_id, votes_count, existing_ids)
            new_achievements.extend(vote_achievements)
            
            # Перевірка досягнень за активністю
            contribution_achievements = await self._check_contribution_achievements(user_id, existing_ids)
            new_achievements.extend(contribution_achievements)
            
            return new_achievements

        except Exception as e:
            logger.error(f"Error checking achievements: {e}")
            return []

    async def get_user_achievements(self, user_id: int) -> List[Dict]:
        """
        Отримання всіх досягнень користувача
        
        Args:
            user_id: ID користувача
        """
        try:
            query = select(UserAchievement, Achievement).join(
                Achievement
            ).where(
                UserAchievement.user_id == user_id
            )
            result = await self._session.execute(query)
            
            achievements = []
            for user_achievement, achievement in result:
                achievements.append({
                    'id': achievement.id,
                    'name': achievement.name,
                    'description': achievement.description,
                    'icon_url': achievement.icon_url,
                    'points': achievement.points,
                    'earned_at': user_achievement.earned_at
                })
            
            return achievements

        except Exception as e:
            logger.error(f"Error getting user achievements: {e}")
            return []

    async def award_achievement(self, user_id: int, achievement_id: int) -> bool:
        """
        Нарахування досягнення користувачу
        
        Args:
            user_id: ID користувача
            achievement_id: ID досягнення
        """
        try:
            # Перевіряємо чи досягнення вже є
            exists_query = select(UserAchievement).where(
                and_(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_id == achievement_id
                )
            )
            result = await self._session.execute(exists_query)
            if result.scalar_one_or_none():
                return False

            # Отримуємо інформацію про досягнення
            achievement_query = select(Achievement).where(Achievement.id == achievement_id)
            achievement_result = await self._session.execute(achievement_query)
            achievement = achievement_result.scalar_one_or_none()
            
            if not achievement:
                return False

            # Створюємо запис про досягнення
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement_id,
                earned_at=datetime.utcnow()
            )
            self._session.add(user_achievement)

            # Нараховуємо бали користувачу
            await self._update_user_points(user_id, achievement.points)
            
            await self.commit()
            logger.info(f"Awarded achievement {achievement_id} to user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error awarding achievement: {e}")
            return False

    async def _count_user_heroes(self, user_id: int) -> int:
        """Підрахунок кількості схвалених героїв користувача"""
        query = select(func.count(Hero.id)).where(
            and_(
                Hero.contributor_id == user_id,
                Hero.status == 'approved'
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def _count_user_votes(self, user_id: int) -> int:
        """Підрахунок загальної кількості голосів за контент користувача"""
        query = select(func.sum(HeroMedia.votes)).where(
            HeroMedia.contributor_id == user_id
        )
        result = await self._session.execute(query)
        return result.scalar_one() or 0

    async def _check_hero_achievements(self, user_id: int, heroes_count: int, existing_ids: List[int]) -> List[Achievement]:
        """Перевірка досягнень за кількістю героїв"""
        achievements = []
        
        hero_milestones = {
            1: "First Hero",
            5: "Hero Collector",
            10: "Hero Master",
            20: "Hero Legend"
        }

        for count, name in hero_milestones.items():
            if heroes_count >= count:
                query = select(Achievement).where(
                    and_(
                        Achievement.name == name,
                        ~Achievement.id.in_(existing_ids)
                    )
                )
                result = await self._session.execute(query)
                achievement = result.scalar_one_or_none()
                if achievement:
                    achievements.append(achievement)

        return achievements

    async def _check_vote_achievements(self, user_id: int, votes_count: int, existing_ids: List[int]) -> List[Achievement]:
        """Перевірка досягнень за кількістю голосів"""
        achievements = []
        
        vote_milestones = {
            10: "Popular Contributor",
            50: "Community Favorite",
            100: "Content Star",
            500: "Legend Creator"
        }

        for count, name in vote_milestones.items():
            if votes_count >= count:
                query = select(Achievement).where(
                    and_(
                        Achievement.name == name,
                        ~Achievement.id.in_(existing_ids)
                    )
                )
                result = await self._session.execute(query)
                achievement = result.scalar_one_or_none()
                if achievement:
                    achievements.append(achievement)

        return achievements

    async def _check_contribution_achievements(self, user_id: int, existing_ids: List[int]) -> List[Achievement]:
        """Перевірка досягнень за активністю"""
        achievements = []
        
        # Отримуємо статистику користувача
        query = select(User).where(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return achievements

        contribution_milestones = {
            10: "Active Contributor",
            50: "Dedicated Contributor",
            100: "Elite Contributor",
            500: "Legendary Contributor"
        }

        for count, name in contribution_milestones.items():
            if user.contribution_count >= count:
                query = select(Achievement).where(
                    and_(
                        Achievement.name == name,
                        ~Achievement.id.in_(existing_ids)
                    )
                )
                result = await self._session.execute(query)
                achievement = result.scalar_one_or_none()
                if achievement:
                    achievements.append(achievement)

        return achievements

    async def _update_user_points(self, user_id: int, points: int) -> bool:
        """Оновлення балів користувача"""
        try:
            query = select(User).where(User.id == user_id)
            result = await self._session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                user.points += points
                await self.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating user points: {e}")
            return False
