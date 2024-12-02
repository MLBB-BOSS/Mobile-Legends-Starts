# utils/hero_loader.py

import os
import json
from typing import List

def get_all_hero_names() -> List[str]:
    """
    Повертає список всіх імен героїв зі всіх класів.
    
    :return: Список імен героїв.
    """
    classes = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank"]
    hero_names = []
    for hero_class in classes:
        directory = os.path.join("heroes", hero_class)
        if not os.path.isdir(directory):
            continue
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                hero_name = os.path.splitext(filename)[0]
                hero_names.append(hero_name)
    return hero_names
