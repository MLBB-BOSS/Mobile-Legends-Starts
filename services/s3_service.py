# services/hero_service.py
import logging
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.hero import Hero
from models.hero_media import HeroMedia
from services.base_service import BaseService
from services.s3_service import S3Service

logger = logging.getLogger(__name__)

class HeroService(BaseService):
    def __init__(self, session: AsyncSession, s3_service: S3Service):
        super().__init__(session)
        self.s3_service = s3_service

    async def create_hero(self, 
                         name: str, 
                         description: str, 
                         contributor_id: int) -> Optional[Hero]:
        """
        Створення нового героя
        
        Args:
            name: Ім'я героя
            description: Опис героя
            contributor_id: ID користувача, який додав героя
        """
        try:
            hero = Hero(
                name=name,
                description=description,
                contributor_id=contributor_id,
                status='pending',
                created_at=datetime.utcnow()
            )
            self._session.add(hero)
            await self.commit()
            logger.info(f"Created new hero: {name}")
            return hero
        except Exception as e:
            logger.error(f"Error creating hero: {e}")
            return None

    async def add_hero_media(self, 
                            hero_id: int, 
                            file_data: bytes,
                            media_type: str,
                            contributor_id: int,
                            content_type: str = 'image/jpeg') -> Optional[HeroMedia]:
        """
        Додавання медіа контенту для героя
        
        Args:
            hero_id: ID героя
            file_data: Байти файлу
            media_type: Тип медіа ('screenshot' або 'skin')
            contributor_id: ID користувача
            content_type: Тип контенту файлу
        """
        try:
            file_key = f"heroes/{hero_id}/{media_type}_{datetime.utcnow().timestamp()}"
            
            # Завантаження файлу в S3
            media_url = await self.s3_service.upload_file(
                file_data=file_data,
                file_key=file_key,
                metadata={
                    'hero_id': str(hero_id),
                    'media_type': media_type,
                    'contributor_id': str(contributor_id)
                },
                content_type=content_type
            )
            
            if not media_url:
                return None

            # Створення запису про медіа
            hero_media = HeroMedia(
                hero_id=hero_id,
                media_type=media_type,
                media_url=media_url,
                contributor_id=contributor_id,
                created_at=datetime.utcnow()
            )
            
            self._session.add(hero_media)
            await self.commit()
            return hero_media

        except Exception as e:
            logger.error(f"Error adding hero media: {e}")
            return None

    async def get_hero(self, hero_id: int) -> Optional[Dict]:
        """
        Отримання інформації про героя
        
        Args:
            hero_id: ID героя
        """
        try:
            query = select(Hero).where(Hero.id == hero_id)
            result = await self._session.execute(query)
            hero = result.scalar_one_or_none()
            
            if not hero:
                return None

            # Отримання медіа контенту
            media_query = select(HeroMedia).where(HeroMedia.hero_id == hero_id)
            media_result = await self._session.execute(media_query)
            media = media_result.scalars().all()

            return {
                'id': hero.id,
                'name': hero.name,
                'description': hero.description,
                'status': hero.status,
                'contributor_id': hero.contributor_id,
                'created_at': hero.created_at,
                'media': [
                    {
                        'id': m.id,
                        'type': m.media_type,
                        'url': m.media_url,
                        'votes': m.votes,
                        'contributor_id': m.contributor_id
                    } for m in media
                ]
            }

        except Exception as e:
            logger.error(f"Error getting hero: {e}")
            return None

    async def update_hero_status(self, 
                                hero_id: int, 
                                status: str,
                                moderator_id: int) -> bool:
        """
        Оновлення статусу героя
        
        Args:
            hero_id: ID героя
            status: Новий статус ('approved' або 'rejected')
            moderator_id: ID модератора
        """
        try:
            query = update(Hero).where(Hero.id == hero_id).values(
                status=status,
                moderator_id=moderator_id,
                moderated_at=datetime.utcnow()
            )
            await self._session.execute(query)
            await self.commit()
            logger.info(f"Updated hero {hero_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating hero status: {e}")
            return False

    async def vote_for_media(self, media_id: int, user_id: int) -> bool:
        """
        Голосування за медіа контент
        
        Args:
            media_id: ID медіа
            user_id: ID користувача
        """
        try:
            query = update(HeroMedia).where(
                HeroMedia.id == media_id
            ).values(
                votes=HeroMedia.votes + 1
            )
            await self._session.execute(query)
            await self.commit()
            return True
        except Exception as e:
            logger.error(f"Error voting for media: {e}")
            return False
