from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.hero import Hero

class HeroRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Hero]:
        """Отримати всіх героїв"""
        result = await self.session.execute(select(Hero))
        return list(result.scalars().all())
    
    async def get_by_class(self, hero_class: str) -> List[Hero]:
        """Отримати героїв певного класу"""
        result = await self.session.execute(
            select(Hero).where(Hero.hero_class == hero_class)
        )
        return list(result.scalars().all())
    
    async def get_by_name(self, name: str) -> Optional[Hero]:
        """Отримати героя за ім'ям"""
        result = await self.session.execute(
            select(Hero).where(Hero.name == name)
        )
        return result.scalar_one_or_none()
    
    async def create(self, hero_data: dict) -> Hero:
        """Створити нового героя"""
        hero = Hero(**hero_data)
        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)
        return hero
