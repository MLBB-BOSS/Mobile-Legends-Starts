# models/contribution.py

import logging
from datetime import datetime
from config.settings import AWS_S3_BUCKET_NAME

logger = logging.getLogger(__name__)

# Для простоти, використаємо просту базу даних SQLite через SQLAlchemy

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Налаштування бази даних
DATABASE_URL = 'sqlite:///contributions.db'  # Замініть на вашу базу даних, якщо потрібно

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Contribution(Base):
    __tablename__ = 'contributions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    contribution_type = Column(String, index=True, nullable=False)
    points = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)
    screenshot_url = Column(String, nullable=True)

    def save(self):
        db = SessionLocal()
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
            logger.info(f"Contribution saved: {self}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving contribution: {e}")
        finally:
            db.close()

    @staticmethod
    def get_user_contributions(user_id):
        db = SessionLocal()
        try:
            contributions = db.query(Contribution).filter(Contribution.user_id == user_id).all()
            return contributions
        except Exception as e:
            logger.error(f"Error fetching contributions for user {user_id}: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_user_badges(user_id):
        # Приклад: видача бейджів за певні досягнення
        contributions = Contribution.get_user_contributions(user_id)
        total_points = sum(c.points for c in contributions)
        badges = []
        if total_points >= 100:
            badges.append("Veteran")
        if total_points >= 50:
            badges.append("Intermediate")
        if total_points >= 10:
            badges.append("Novice")
        return badges

    @staticmethod
    def get_top_users(limit=10):
        db = SessionLocal()
        try:
            from sqlalchemy import func
            top_users = db.query(
                Contribution.user_id,
                func.sum(Contribution.points).label('total_points')
            ).group_by(Contribution.user_id).order_by(func.sum(Contribution.points).desc()).limit(limit).all()
            # Для кожного користувача можна отримати username, якщо зберігається
            # Тут будемо просто повертати user_id та total_points
            return top_users
        except Exception as e:
            logger.error(f"Error fetching top users: {e}")
            return []
        finally:
            db.close()

# Створення таблиці, якщо вона не існує
Base.metadata.create_all(bind=engine)
