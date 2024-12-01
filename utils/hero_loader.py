# utils/hero_loader.py

import os
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Шлях до папки з героями
HEROES_DIR = os.path.join(os.path.dirname(__file__), '..', 'heroes')

def load_heroes() -> Dict[str, Dict[str, Any]]:
    """
    Завантажує дані про героїв з JSON-файлів, організованих за класами.
    
    :return: Словник з класами героїв, кожен з яких містить героїв та їхні дані.
    """
    heroes_data = {}
    try:
        for class_name in os.listdir(HEROES_DIR):
            class_path = os.path.join(HEROES_DIR, class_name)
            if os.path.isdir(class_path):
                heroes_data[class_name] = {}
                for hero_file in os.listdir(class_path):
                    if hero_file.endswith('.json'):
                        hero_path = os.path.join(class_path, hero_file)
                        with open(hero_path, 'r', encoding='utf-8') as f:
                            hero_info = json.load(f)
                            hero_name = hero_info.get('name')
                            if hero_name:
                                heroes_data[class_name][hero_name] = hero_info
                            else:
                                logger.warning(f"Файл {hero_file} не містить ключа 'name'.")
    except Exception as e:
        logger.error(f"Помилка при завантаженні героїв: {e}")
    logger.info(f"Завантажено {sum(len(heroes) for heroes in heroes_data.values())} героїв.")
    return heroes_data

# Завантаження героїв при імпорті модуля
HEROES = load_heroes()
