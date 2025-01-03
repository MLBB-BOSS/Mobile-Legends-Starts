# utils/tasks.py
from utils.db import get_sync_db

def update_user_stats(user_id: int):
    with get_sync_db() as db:
        user = db.query(User).get(user_id)
        if user:
            # Оновлення статистики
            user.matches_count += 1
            db.commit()
