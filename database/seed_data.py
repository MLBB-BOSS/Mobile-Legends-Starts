import asyncio
from database.connection import AsyncSessionLocal
from database.models.hero import Hero

# Початкові дані героїв
initial_heroes = [
    {
        "name": "Alucard",
        "hero_class": "Fighter",
        "role": "Fighter/Assassin",
        "specialty": "Reap/Chase",
        "difficulty": 3,
        "description": "A demon hunter who wields a giant sword",
        "image_url": "https://example.com/alucard.jpg",
        "hp": 2669,
        "mana": 0,
        "physical_attack": 124,
        "magic_power": 0,
        "armor": 23,
        "magic_resistance": 0,
        "movement_speed": 255
    },
    {
        "name": "Miya",
        "hero_class": "Marksman",
        "role": "Marksman",
        "specialty": "Damage/Attack Speed",
        "difficulty": 2,
        "description": "An elven archer with rapid-fire abilities",
        "image_url": "https://example.com/miya.jpg",
        "hp": 2541,
        "mana": 100,
        "physical_attack": 132,
        "magic_power": 0,
        "armor": 17,
        "magic_resistance": 0,
        "movement_speed": 250
    }
    # Додайте інших героїв за потреби
]

async def seed_database():
    """Заповнення бази даних початковими даними"""
    async with AsyncSessionLocal() as session:
        for hero_data in initial_heroes:
            hero = Hero(**hero_data)
            session.add(hero)
        
        await session.commit()
    
    print("Базу даних успішно заповнено початковими даними!")

# Запускаємо заповнення даними
if __name__ == "__main__":
    asyncio.run(seed_database())
