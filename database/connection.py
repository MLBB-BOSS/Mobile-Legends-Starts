from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Замінюємо postgresql:// на postgresql+asyncpg:// для асинхронного з'єднання
DATABASE_URL = settings.DATABASE_URL.replace(
    'postgresql://', 
    'postgresql+asyncpg://', 
    1
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
