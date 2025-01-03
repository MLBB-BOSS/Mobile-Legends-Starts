# utils/db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from dotenv import load_dotenv

# Завантажте змінні середовища з .env файлу (для локальної розробки)
load_dotenv()

# Отримайте URL бази даних з змінної середовища AS_BASE
DATABASE_URL = os.getenv('AS_BASE')

if not DATABASE_URL:
    raise ValueError("Не встановлено змінну середовища AS_BASE")

# Створіть асинхронний двигун SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Створіть фабрику асинхронних сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    # Імпортуйте моделі після визначення Base та engine, щоб уникнути циклічних імпортів
    import utils.models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def check_connection():
    try:
        async with engine.connect() as connection:
            return True
    except Exception as e:
        print(f"Підключення до бази даних не вдалося: {e}")
        return False