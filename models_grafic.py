# models.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text
import os

DATABASE_URL = os.getenv('DATABASE_URL')  # Формат: postgresql+asyncpg://user:password@host/dbname

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)

class Build(Base):
    __tablename__ = 'builds'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    hero = Column(String)
    build_details = Column(Text)

# Створення таблиць (запустіть окремо)
# import asyncio
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.run(init_db())
