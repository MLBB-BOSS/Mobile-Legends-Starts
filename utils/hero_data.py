# utils/hero_data.py

import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def load_hero_data(hero_name: str) -> Dict[str, Any]:
    """
    Завантажує базову інформацію про героя з відповідного JSON-файлу.
    
    :param hero_name: Назва героя.
    :return: Словник з даними героя або порожній словник, якщо герой не знайдений.
    """
    classes = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank"]
    for hero_class in classes:
        filepath = os.path.join("heroes", hero_class, f"{hero_name}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                logger.info(f"Завантажено дані для героя: {hero_name}")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Помилка декодування JSON для героя {hero_name}: {e}")
                return {}
    logger.warning(f"Герой {hero_name} не знайдений у жодному класі.")
    return {}
