# tests/conftest.py

import pytest
from myapp import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app
    # Додаткові дії після тесту, якщо необхідно
