# tests/test_handlers.py

import pytest
from aiogram.types import Message, CallbackQuery
from handlers.basic_handlers import start_command
from handlers.hero_handler import heroes_command, process_class_selection, back_to_classes, process_hero_selection

class MockMessage:
    async def reply(self, text):
        return text

class MockCallbackQuery:
    def __init__(self, data):
        self.data = data
    async def answer(self, text):
        return text

@pytest.mark.asyncio
async def test_start_command():
    message = MockMessage()
    response = await start_command(message)
    assert response == "Вітаю! Я ваш бот, готовий допомогти."

@pytest.mark.asyncio
async def test_heroes_command():
    message = MockMessage()
    response = await heroes_command(message)
    assert response == "Оберіть клас персонажів:"

@pytest.mark.asyncio
async def test_process_class_selection():
    call = MockCallbackQuery("class_Assassin")
    response = await process_class_selection(call)
    assert response == "Оберіть персонажа з класу Assassin:"

@pytest.mark.asyncio
async def test_back_to_classes():
    call = MockCallbackQuery("back_to_classes")
    response = await back_to_classes(call)
    assert response == "Оберіть клас персонажів:"

@pytest.mark.asyncio
async def test_process_hero_selection():
    call = MockCallbackQuery("hero_Aamon")
    response = await process_hero_selection(call)
    assert response == "Ви обрали героя Aamon. Додаткова інформація буде додана."
