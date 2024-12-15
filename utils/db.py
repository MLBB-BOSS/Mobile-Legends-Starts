# utils/db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Змінна середовища або хардкоджений URL — краще зберігати у змінних середовища
AS_BASE = os.getenv("AS_BASE", "postgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd")

if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid")

engine = create_async_engine(AS_BASE, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncSession:
    return async_session()