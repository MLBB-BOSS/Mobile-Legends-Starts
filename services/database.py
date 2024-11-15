from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
import os

# Використовуємо ваш URL для асинхронної бази даних
ASYNC_DATABASE_URL = "postgresql+asyncpg://u19gdelo8pjkrg:pb95edc1e9dc17f2d21f8f49fe9e9c6a3c2eab4969e95adbfc2c69a5c753b9fdb@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/da4c4gk6ldknbt"

# Створюємо асинхронний двигун
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    nickname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    game_id = Column(String, unique=True, nullable=False)
    is_registered = Column(Boolean, default=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
