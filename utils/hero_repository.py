import json
from pathlib import Path

class HeroRepository:
    HEROES_DIR = Path("heroes")  # Директорія з героями (наприклад, heroes/Assassin, heroes/Fighter тощо)

    @classmethod
    def load_hero_data(cls, hero_class: str) -> dict:
        """
        Завантажує дані героїв певного класу.

        :param hero_class: Назва класу героя (наприклад, "Assassin", "Tank").
        :return: Словник з даними героїв.
        """
        hero_path = cls.HEROES_DIR / hero_class
        hero_data = {}

        if hero_path.exists() and hero_path.is_dir():
            for hero_file in hero_path.glob("*.json"):
                with open(hero_file, "r", encoding="utf-8") as f:
                    hero_data[hero_file.stem] = json.load(f)
        return hero_data

    @classmethod
    def get_all_heroes(cls) -> dict:
        """
        Завантажує дані про всіх героїв із різних класів.

        :return: Словник з усіма героями, згрупованими за класами.
        """
        all_heroes = {}
        for hero_class in cls.HEROES_DIR.iterdir():
            if hero_class.is_dir():
                all_heroes[hero_class.name] = cls.load_hero_data(hero_class.name)
        return all_heroes
