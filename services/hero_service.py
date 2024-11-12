# services/hero_service.py

import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from models import Hero, HeroMedia
from services.s3_service import S3Service

logger = logging.getLogger(__name__)

class HeroService:
    def __init__(self):
        self.s3_service = S3Service()
        self._heroes: Dict[str, Hero] = {}  # Тимчасове зберігання для прототипу
        
    async def create_hero(self, hero_data: Dict[str, Any]) -> Hero:
        """Створення нового героя"""
        try:
            hero = Hero(
                name=hero_data['name'],
                role=hero_data['role'],
                description=hero_data['description'],
                difficulty=hero_data.get('difficulty', 'Normal'),
                speciality=hero_data.get('speciality', []),
                recommended_spells=hero_data.get('recommended_spells', []),
                recommended_emblems=hero_data.get('recommended_emblems', [])
            )
            self._heroes[hero.id] = hero
            return hero
        except Exception as e:
            logger.error(f"Error creating hero: {e}")
            raise

    async def get_hero(self, hero_id: str) -> Optional[Hero]:
        """Отримання героя за ID"""
        return self._heroes.get(hero_id)

    async def get_heroes(self) -> List[Hero]:
        """Отримання всіх героїв"""
        return list(self._heroes.values())

    async def update_hero(self, hero_id: str, hero_data: Dict[str, Any]) -> Optional[Hero]:
        """Оновлення інформації про героя"""
        hero = await self.get_hero(hero_id)
        if hero:
            for key, value in hero_data.items():
                if hasattr(hero, key):
                    setattr(hero, key, value)
            hero.updated_at = datetime.utcnow()
            return hero
        return None

    async def add_hero_media(self, 
                           hero_id: str, 
                           file_data: bytes, 
                           media_type: str,
                           author_id: str,
                           author_nickname: str,
                           metadata: Dict = None) -> Optional[HeroMedia]:
        """Додавання медіа контенту для героя"""
        try:
            hero = await self.get_hero(hero_id)
            if not hero:
                raise ValueError(f"Hero with id {hero_id} not found")

            # Завантаження файлу в S3
            file_key = f"heroes/{hero_id}/{media_type}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            url = await self.s3_service.upload_file(
                file_data,
                file_key,
                metadata={
                    'hero_id': hero_id,
                    'media_type': media_type,
                    'author_id': author_id
                }
            )

            if not url:
                raise Exception("Failed to upload file to S3")

            # Створення запису про медіа
            hero_media = HeroMedia(
                hero_id=hero_id,
                media_type=media_type,
                url=url,
                author_id=author_id,
                author_nickname=author_nickname,
                metadata=metadata or {}
            )

            # Оновлення лічильника медіа для героя
            hero.media_count += 1
            
            return hero_media

        except Exception as e:
            logger.error(f"Error adding hero media: {e}")
            raise

    async def get_hero_media(self, 
                           hero_id: str, 
                           media_type: Optional[str] = None,
                           approved_only: bool = True) -> List[HeroMedia]:
        """Отримання медіа контенту героя"""
        # В реальному проекті тут буде запит до бази даних
        # Зараз повертаємо пустий список для прототипу
        return []

    async def approve_media(self,
                          media_id: str,
                          approver_id: str) -> Optional[HeroMedia]:
        """Затвердження медіа контенту"""
        # В реальному проекті тут буде логіка затвердження
        # Зараз повертаємо None для прототипу
        return None

    async def vote_for_media(self,
                           media_id: str,
                           user_id: str) -> bool:
        """Голосування за медіа контент"""
        # В реальному проекті тут буде логіка голосування
        # Зараз повертаємо False для прототипу
        return False

    async def search_heroes(self, query: str) -> List[Hero]:
        """Пошук героїв"""
        query = query.lower()
        return [
            hero for hero in self._heroes.values()
            if query in hero.search_text
        ]

    async def get_popular_heroes(self, limit: int = 10) -> List[Hero]:
        """Отримання популярних героїв"""
        heroes = list(self._heroes.values())
        heroes.sort(key=lambda x: x.popularity, reverse=True)
        return heroes[:limit]
