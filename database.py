from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings

# Створення асинхронного двигуна
engine = create_async_engine(settings.db_url, echo=settings.DEBUG)

# Фабрика асинхронних сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)