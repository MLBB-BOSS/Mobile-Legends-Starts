name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Клонувати репозиторій
      uses: actions/checkout@v3

    - name: Встановити Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Встановити залежності
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Перевірити структуру коду
      run: |
        python scripts/check_code.py .py
      # Цей крок виведе вміст усіх .py файлів у логах

    - name: Запустити тести
      run: |
        export PYTHONPATH="${PYTHONPATH}:${GITHUB_WORKSPACE}"
        pytest -v

    - name: Завантажити результати тестів
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: tests/__pycache__/

    - name: Сповістити про помилку у Slack
      if: failure()
      uses: rtCamp/action-slack-notify@v2
      env:
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_MESSAGE: '❌ Помилка конвеєра CI/CD для `MLBB-BOSS/Mobile-Legends-Starts-` на `refs/heads/main`.'
        SLACK_USERNAME: 'GitHub Actions'
        SLACK_ICON_EMOJI: ':red_circle:'
