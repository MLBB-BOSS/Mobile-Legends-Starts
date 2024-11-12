# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os
from typing import Generator

class DatabaseConnection:
    def __init__(self):
        self._engine = None
        self._session_factory = None
        
    def init_db(self, database_url: str = None):
        if not database_url:
            database_url = os.getenv('DATABASE_URL')
            
        if not database_url:
            raise ValueError("Database URL is not provided")
            
        self._engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
        
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
        )
    
    @contextmanager
    def get_session(self) -> Generator:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            
    def close(self):
        if self._engine:
            self._engine.dispose()

# Створюємо глобальний екземпляр підключення
db = DatabaseConnection()
