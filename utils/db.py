# utils/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from dotenv import load_dotenv

# Завантажте змінні середовища з .env файлу (для локальної розробки)
load_dotenv()

# Отримайте URL бази даних з змінної середовища
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("Не встановлено змінну середовища DATABASE_URL")

# Створіть двигун SQLAlchemy
engine = create_engine(DATABASE_URL)

# Створіть фабрику сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Імпортуйте моделі після визначення Base та engine, щоб уникнути циклічних імпортів
    import utils.models
    Base.metadata.create_all(bind=engine)

def check_connection():
    try:
        with engine.connect() as connection:
            return True
    except Exception as e:
        print(f"Підключення до бази даних не вдалося: {e}")
        return False