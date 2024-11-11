# core/screenshot_handler.py

from models.contribution import Contribution
from services.database import get_db

def handle_screenshot(user_id, screenshot_path, db):
    # Логіка для обробки скріншотів
    contribution = Contribution(user_id=user_id, contribution_type="screenshot", points=5, date="2024-11-11")
    db.add(contribution)
    db.commit()
    return f"Скріншот додано користувачем {user_id}!"
