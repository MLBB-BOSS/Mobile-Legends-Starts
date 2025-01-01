# texts/utils.py

def generate_heroes_list(hero_class: str, heroes: List[Dict[str, str]]) -> str:
    """Функція для генерації списку героїв з їхніми описами."""
    heroes_info = ""
    for idx, hero in enumerate(heroes, start=1):
        heroes_info += f"• <b>{hero['name']}:</b> {hero['description']}\n"
    return heroes_info
