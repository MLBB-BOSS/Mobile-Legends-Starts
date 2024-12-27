# create_docs_structure.py

import os
from datetime import datetime

class DocsGenerator:
    def __init__(self):
        self.base_path = "docs"
        self.current_date = "2024-12-27 20:13:32"  # Оновлений час
        self.project_name = "Mobile-Legends-Stats"
        self.author = "MLBB-BOSS"
        self.bot_name = "@MLBB_MLS_BOT"
        self.branch = "aiogram-3x"

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

    def create_base_files(self):
        readme_content = f"""# {self.project_name} Documentation

## Bot Information
- **Bot Name:** {self.bot_name}
- **Generated:** {self.current_date}
- **Author:** {self.author}
- **Branch:** {self.branch}

## Project Structure 🏢

Our bot is structured like a 99-floor building:

1. **Main Block (1-20)** 🏠
   - Main menu and core functionality
   - Settings and user preferences
   - Profile and statistics
   
2. **Historical Block (21-26)** 🏰
   - Tournament system
   - Heroes menu
   - Counter picks
   
3. **New Construction (27-28)** 🆕
   - Meta game features
   - M6 section

4. **Additional Block (29-32)** 🏗
   - Hero list in meta menu
   - Recommendations
   - Updates menu
   
[... continues with all blocks]

## Documentation Structure

- 📁 **api/** - API documentation
- 📁 **user-guide/** - End user documentation
- 📁 **admin-guide/** - Administrator documentation
- 📁 **developer-guide/** - Developer documentation
- 📁 **deployment/** - Deployment instructions
- 📁 **states/** - States documentation (our 99 "apartments")
- 📁 **handlers/** - Handlers documentation
- 📁 **database/** - Database structure
- 📁 **utils/** - Utilities documentation

## Quick Links
- [States Documentation](states/README.md)
- [Handlers Documentation](handlers/README.md)
- [User Guide](user-guide/README.md)
- [Admin Guide](admin-guide/README.md)
"""
        with open(os.path.join(self.base_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

    def create_states_docs(self):
        states_content = """# States Documentation

## Overview 🏢

Total states: 99
Last updated: {self.current_date}

## Building Structure

### 1. Main Block (1-20) 🏠
```python
MAIN_MENU = State()                 # 1. Головне меню користувача
CHALLENGES_MENU = State()           # 2. Меню викликів
# ... [all states listed with numbers]
