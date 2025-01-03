# utils/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base  # Імпорт базового класу
from .models.user import User

engine = create_engine('postgresql://user:password@host:port/dbname')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import utils.models  # Імпорт моделей після налаштування бази
    Base.metadata.create_all(bind=engine)

def check_connection():
    try:
        engine.connect()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
