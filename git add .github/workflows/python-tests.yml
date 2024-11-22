name: Run Python Script

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      # Клонуйте репозиторій
      - name: Checkout code
        uses: actions/checkout@v3

      # Встановіть Python
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10  # Вкажіть версію Python

      # Встановіть залежності
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Запустіть скрипт
      - name: Run the script
        run: |
          python core/bot_runner.py
