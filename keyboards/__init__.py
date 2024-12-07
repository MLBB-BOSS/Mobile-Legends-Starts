mlbb.boss.ua@gmail.com
2024-12-07T10:50:09.855395+00:00 heroku[worker.1]: State changed from crashed to starting
2024-12-07T10:50:16.974163+00:00 heroku[worker.1]: Starting process with command `python bot.py`
2024-12-07T10:50:17.561289+00:00 heroku[worker.1]: State changed from starting to up
2024-12-07T10:50:20.282729+00:00 app[worker.1]: Traceback (most recent call last):
2024-12-07T10:50:20.282754+00:00 app[worker.1]:   File "/app/bot.py", line 12, in <module>
2024-12-07T10:50:20.282786+00:00 app[worker.1]:     from handlers import setup_handlers
2024-12-07T10:50:20.282803+00:00 app[worker.1]:   File "/app/handlers/__init__.py", line 3, in <module>
2024-12-07T10:50:20.282834+00:00 app[worker.1]:     from .base import setup_handlers
2024-12-07T10:50:20.282846+00:00 app[worker.1]:   File "/app/handlers/base.py", line 34, in <module>
2024-12-07T10:50:20.282898+00:00 app[worker.1]:     from texts import (
2024-12-07T10:50:20.282907+00:00 app[worker.1]: ImportError: cannot import name 'PROFILE_MENU_TEXT' from 'texts' (/app/texts.py)
2024-12-07T10:50:20.562334+00:00 heroku[worker.1]: Process exited with status 1
2024-12-07T10:50:20.580295+00:00 heroku[worker.1]: State changed from up to crashed
