from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.base import BaseModel
import logging

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Базовий сервіс для роботи з моделями
        
        Args:
            model: Клас моделі
            db: Сесія бази даних
        """
        self.model = model
        self.db = db
        
    async def create(self, **data) -> ModelType:
        """
        Створення нового запису
        
        Args:
            **data: Дані для створення
            
        Returns:
            Створений об'єкт
        """
        try:
            obj = self.model(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise

    async def get(self, id: int) -> ModelType:
        """
        Отримання запису за ID
        
        Args:
            id: Ідентифікатор запису
            
        Returns:
            Знайдений об'єкт або None
        """
        return await self.db.query(self.model).filter(self.model.id == id).first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        """
        Отримання всіх записів з пагінацією
        
        Args:
            skip: Кількість записів для пропуску
            limit: Максимальна кількість записів
            
        Returns:
            Список об'єктів
        """
        return await self.db.query(self.model).offset(skip).limit(limit).all()

    async def update(self, id: int, **data) -> ModelType:
        """
        Оновлення запису
        
        Args:
            id: Ідентифікатор запису
            **data: Дані для оновлення
            
        Returns:
            Оновлений об'єкт
        """
        try:
            obj = await self.get(id)
            if not obj:
                return None
                
            for key, value in data.items():
                setattr(obj, key, value)
                
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise

    async def delete(self, id: int) -> bool:
        """
        Видалення запису
        
        Args:
            id: Ідентифікатор запису
            
        Returns:
            True якщо запис видалено, False якщо запис не знайдено
        """
        try:
            obj = await self.get(id)
            if not obj:
                return False
                
            await self.db.delete(obj)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            raise

    async def exists(self, id: int) -> bool:
        """
        Перевірка існування запису
        
        Args:
            id: Ідентифікатор запису
            
        Returns:
            True якщо запис існує, False якщо ні
        """
        return await self.db.query(self.model).filter(self.model.id == id).first() is not None

    async def count(self) -> int:
        """
        Підрахунок кількості записів
        
        Returns:
            Кількість записів
        """
        return await self.db.query(self.model).count()

    async def filter(self, **filters):
        """
        Фільтрація записів
        
        Args:
            **filters: Фільтри у форматі {поле: значення}
            
        Returns:
            Список відфільтрованих об'єктів
        """
        query = self.db.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return await query.all()
