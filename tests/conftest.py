# tests/conftest.py

import sys
import os
import pytest

# Додавання кореневої директорії до sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myapp import create_app  # Переконайтеся, що шлях правильний

@pytest.fixture
def app():
    app = create_app()
    return app
