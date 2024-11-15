import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database.base import Base
from database.models.hero import Hero
from config.settings import settings

async def init_database():
    """Ініціалізація бази даних та створення всіх таблиць"""
    # Створюємо двигун
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG
    )
    
    async with engine.begin() as conn:
        # Видаляємо всі існуючі таблиці
        await conn.run_sync(Base.metadata.drop_all)
        # Створюємо нові таблиці
        await conn.run_sync(Base.metadata.create_all)
        
    await engine.dispose()
    
    print("База даних успішно ініціалізована!")

# Запускаємо ініціалізацію
if __name__ == "__main__":
    asyncio.run(init_database())
