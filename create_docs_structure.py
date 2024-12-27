# create_docs_structure.py

import os
from datetime import datetime

class DocsGenerator:
    def __init__(self):
        self.base_path = "docs"
        self.current_date = "2024-12-27 20:09:26"  # Оновлено згідно з вашими даними
        self.project_name = "Mobile-Legends-Stats"
        self.author = "MLBB-BOSS"
        self.bot_name = "@MLBB_MLS_BOT"
        self.branch = "aiogram-3x"
        self.heroku_app = "mlbb"

    def create_directory_structure(self):
        directories = [
            "",
            "/api",
            "/user-guide",
            "/admin-guide",
            "/developer-guide",
            "/deployment",
            "/states",
            "/handlers",
            "/database",
            "/utils"
        ]

        for dir_path in directories:
            full_path = os.path.join(self.base_path, dir_path.lstrip("/"))
            os.makedirs(full_path, exist_ok=True)

    def create_deployment_docs(self):
        deployment_content = f"""# Deployment Guide

## Heroku Deployment

### Application Information
- **App Name:** {self.heroku_app}
- **Branch:** {self.branch}
- **Last Deploy:** {self.current_date}

### Deployment Process
1. Push to branch `{self.branch}`
2. GitHub Actions automatically:
   - Generates documentation
   - Deploys to Heroku

### Manual Deployment
```bash
heroku git:remote -a {self.heroku_app}
git push heroku {self.branch}:main --force
