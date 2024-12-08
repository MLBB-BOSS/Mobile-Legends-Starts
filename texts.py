# texts.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Початок імпорту функцій з keyboards.menus...")
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    # інші функції
)
logger.info("Імпорт завершено успішно.")

# Привітальні повідомлення
INTRO_PAGE_1_TEXT = (
    """\ud83d\udd25 <b>Mobile Legends: Starts!</b> 
    
\ud83c\udfae \u0422\u0438 \u0449\u043e\u0439\u043d\u043e \u0432\u0456\u0434\u043a\u0440\u0438\u0432 \u0434\u0432\u0435\u0440\u0456 \u0443 \u0441\u0432\u0456\u0442 \u043d\u043e\u0432\u0438\u0445 \u043c\u043e\u0436\u043b\u0438\u0432\u043e\u0441\u0442\u0435\u0439. Mobile Legends: Starts \u2013 \u0446\u0435 \u043d\u0435 \u043f\u0440\u043e\u0441\u0442\u043e \u0431\u043e\u0442, \u0446\u0435 \u0442\u0432\u0456\u0439 \u043d\u043e\u0432\u0438\u0439 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u0438\u0439 \u043f\u0430\u0440\u0442\u043d\u0435\u0440 \u0443 \u043f\u0456\u0434\u043a\u043e\u0440\u0435\u043d\u043d\u0456 \u0432\u0441\u0435\u0441\u0432\u0456\u0442\u0443 Mobile Legends: Bang Bang (MLBB). \u0413\u043e\u0442\u0443\u0439\u0441\u044f \u0434\u043e \u043d\u0435\u0439\u043c\u043e\u0432\u0456\u0440\u043d\u043e\u0433\u043e \u0434\u043e\u0441\u0432\u0456\u0434\u0443, \u044f\u043a\u0438\u0439 \u0437\u043c\u0456\u043d\u0438\u0442\u044c \u0442\u0432\u043e\u0454 \u0441\u043f\u0440\u0438\u0439\u043d\u044f \u0433\u0440\u0438!
    
\u0427\u043e\u043c\u0443 \u0446\u0435 \u0443\u043d\u0456\u043a\u0430\u043b\u044c\u043d\u043e?
    
\ud83d\udd39 \u041f\u0435\u0440\u0448\u0435 \u0432 \u0441\u0432\u0456\u0442\u0456 MLBB-\u0440\u0456\u0448\u0435\u043d\u043d\u044f \u0432 Telegram: \u041c\u0438 \u0441\u0442\u0432\u043e\u0440\u0438\u043b\u0438 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u0443, \u044f\u043a\u0430 \u043f\u043e\u0454\u0434\u043d\u0443\u0454 \u0432 \u0441\u043e\u0431\u0456 \u043d\u0430\u0439\u043d\u043e\u0432\u0456\u0448\u0456 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0456\u0457 \u0448\u0442\u0443\u0447\u043d\u043e\u0433\u043e \u0456\u043d\u0442\u0435\u043b\u0435\u043a\u0442\u0443 (GPT), \u0442\u0432\u043e\u0457 \u043f\u043e\u0442\u0440\u0435\u0431\u0438 \u044f\u043a \u0433\u0440\u0430\u0432\u0446\u044f \u0442\u0430 \u0456\u043d\u0442\u0443\u0457\u0442\u0438\u0432\u043d\u0438\u0439 \u0456\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441.
\ud83d\udd39 \u0414\u043b\u044f \u0433\u0440\u0430\u0432\u0446\u0456\u0432 \u0456 \u0444\u0430\u043d\u0430\u0442\u0456\u0432: \u0426\u0435 \u043c\u0456\u0441\u0446\u0435, \u0434\u0435 \u0442\u0438 \u0437\u043d\u0430\u0439\u0434\u0435\u0448 \u0443\u0441\u0435 \u2013 \u0432\u0456\u0434 \u0431\u0456\u043b\u0434\u0456\u0432 \u0456 \u0433\u0430\u0439\u0434\u0456\u0432 \u0434\u043e \u0456\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u0438\u0445 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0439 \u0456 \u0442\u0443\u0440\u043d\u0456\u0440\u0456\u0432.
\ud83d\udd39 \u041f\u0435\u0440\u0448\u043e\u043a\u043b\u0430\u0441\u043d\u0438\u0439 \u0428\u0406: \u041d\u0430\u0448 GPT \u0433\u043e\u0442\u043e\u0432\u0438\u0439 \u0432\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u0430\u0442\u0438 \u043d\u0430 \u0442\u0432\u043e\u0457 \u0437\u0430\u043f\u0438\u0442\u0430\u043d\u043d\u044f, \u0434\u0430\u0432\u0430\u0442\u0438 \u043f\u043e\u0440\u0430\u0434\u0438 \u0442\u0430 \u043d\u0430\u0432\u0456\u0442\u044c \u0433\u0435\u043d\u0435\u0440\u0443\u0432\u0430\u0442\u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0456\u0437\u043e\u0432\u0430\u043d\u0456 \u0440\u0456\u0448\u0435\u043d\u043d\u044f.
    """
)

INTRO_PAGE_2_TEXT = (
    """---
    
\u0429\u043e \u0442\u0438 \u043d\u0430\u0439\u0434\u0435\u0448\u044c \u0443 Mobile Legends: Starts?
    
\ud83e\udd8a <b>\u0413\u0435\u0440\u043e\u0439\u0438:</b>
    
\u0414\u0438\u0437\u043d\u0430\u0439\u0441\u044f \u043f\u0440\u043e \u0441\u043b\u0438\u0448\u043d\u0456 \u0442\u0440\u043e\u043d\u0438 \u0441\u0435\u0440\u0448\u043d\u0456 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430.
    
\u042f\u043a\u0456 \u0433\u0435\u0440\u043e\u0439\u0438 \u043d\u0430\u0439\u043a\u0440\u0430\u0441\u0442\u0456 \u043f\u043e\u0434\u043e\u0434\u0456\u0436\u0443\u0442\u044c \u044f\u043a \u0442\u0432\u043e\u0454 \u0441\u0442\u0438\u043b\u044c \u0433\u0440\u0438? GPT \u043e\u0434\u043d\u0430\u0448\u043e \u0437\u0430\u043f\u0440\u043e\u043f\u043e\u0437\u0443\u0435 \u043e\u043f\u0442\u0456\u043c\u0430\u043b\u044c\u043d\u0456 \u0432\u0430\u0440\u0456\u0430\u043d\u0442\u0438, \u0432\u0443\u0447\u0430\u043b\u044f\u0447\u0438 \u043f\u043e\u0442\u043e\u0447\u043d\u0443\u044e \u043c\u0435\u0442\u0443 \u0433\u0440\u0438!
    
\u0421\u0435\u043a\u0440\u0435\u0442\u043d\u0456 \u0442\u0440\u044e\u043a\u0438 \u0442\u0430 \u043a\u043e\u043c\u0431\u0456\u043d\u0430\u0446\u0456\u0457 \u0434\u043b\u044f \u0434\u043e\u043c\u043e\u043d\u0456\u0432\u0430\u043d\u043d\u0456\u044f \u0432 \u0431\u043e\u044e.
    
\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440:
<i>"\u042f \u0433\u0440\u0430\u044e \u0437\u0430 \u041c\u0438\u0434\u043b\u0435\u0439\u043d, \u043d\u043e \u043d\u0435 \u043c\u043e\u0433\u0443 \u0432\u0438\u0431\u0440\u0430\u0442\u0438 \u0433\u0435\u0440\u043e\u044f. \u0429\u043e \u043f\u043e\u043b\u0430\u0434\u0438\u0448?"</i>
GPT \u043e\u0434\u043d\u0430\u0448\u043e \u0437\u0430\u043f\u0440\u043e\u043f\u043e\u0437\u0443\u0435 \u043e\u043f\u0442\u0456\u043c\u0430\u043b\u044c\u043d\u0456 \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u0438, \u0432\u0443\u0447\u0430\u043b\u044f\u0447\u0438 \u043f\u043e\u0442\u043e\u0447\u043d\u0443\u044e \u043c\u0435\u0442\u0443 \u0433\u0440\u0438.
    """
)

INTRO_PAGE_3_TEXT = (
    """---
    
\ud83d\udcdc <b>\u0413\u0430\u0439\u0434\u0438 \u0442\u0430 \u0431\u0438\u043b\u0434\u0438:</b>
    
\u041e\u0442\u043c\u0438\u0442\u044c \u0434\u0435\u0442\u0430\u043b\u0456\u0435 \u0433\u0430\u0439\u0434\u0438 \u0434\u043b\u044f \u0431\u0443\u0434\u043e\u0439 \u0442\u0438 \u0440\u043e\u043b\u0456.
    
\u0413\u0435\u043d\u0435\u0440\u0443\u0439 \u0431\u0438\u043b\u0434\u0438 \u043f\u0443\u0434 \u0441\u0432\u0456\u044e \u0441\u0442\u0438\u043b\u044c \u0433\u0440\u0438 \u0447\u0438 \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u0456 \u0441\u0443\u0442\u0430\u0446\u0456\u0457.
    
\u0413\u043e\u0442\u043e\u0432\u0456 \u0440\u0456\u0448\u0435\u043d\u043d\u044f \u0434\u043b\u044f \u0448\u0442\u0440\u043e\u0439\u043a\u043e\u0433\u043e \u0441\u0442\u0430\u0440\u0442\u0443 \u0442\u0430 \u043e\u0441\u043e\u0441\u043d\u0443\u0432\u0430\u043d\u043d\u044f \u043d\u043e\u0432\u0438\u0445 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0439.
    
\u0417\u0430\u0434\u0430\u0439 \u0413\u041f\u0422 \u043f\u0456\u0441\u044f\u043d\u043d\u044f:
<i>"\u041a\u0430\u043a \u043f\u0440\u0430\u043f\u0438\u043b\u044c\u043d\u043e \u0437\u0431\u0438\u0440\u0430\u0442\u0438 \u041b\u0435\u0441\u044c\u0441\u0438 \u0434\u043b\u044f \u0430\u0433\u0440\u0435\u0441\u0456\u0432\u043d\u0456\u0445 \u0433\u0440\u0438?"</i>
GPT \u0441\u0442\u043e\u0440\u0438\u0442\u044c \u0456\u043f\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0438\u0439 \u0431\u0438\u043b\u0434 \u0456\u0437 \u043f\u043e\u044f\u0441\u043d\u0435\u043d\u043d\u044f\u043c\u0438.
    
---
    
\u041a\u0430\u043a \u043f\u043e\u0447\u0430\u0442\u0430\u0442\u0438?
    
1. \u041d\u0430\u0442\u0438\u0441\u043d\u0438 \u043a\u043e\u043b\u043e\u043a\u0443 <b>"\u0420\u043e\u0437\u043f\u043e\u0447\u0430\u0442\u0430\u0442\u0438 \ud83d\ude80"</b>.
    
2. \u0417\u0430\u0434\u0430\u0439 \u043f\u0435\u0440\u0448\u0435 \u0437\u0430\u043f\u0438\u0442\u0430\u043d\u043d\u044f \u043e\u0440\u0430 \u0434\u043e\u0441\u043e\u0433\u0434\u0438 \u0444\u0443\u043d\u043a\u0446\u0456\u0457 \u0431\u043e\u0442\u0430.
    
3. \u041e\u0442\u043c\u0438\u0442\u044c \u0432\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u0438, \u0456\u0434\u0435\u044f \u0442\u0430 \u0434\u043e\u043f\u043e\u043c\u043e\u0433\u0443 \u0432 \u0440\u043e\u0437\u043c\u0456\u043d\u0454 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0438\u0434\u0430\u0442\u043a\u0443.
    
---
    
\u0422\u0432\u0438\u0439 \u043d\u043e\u0432\u0438\u0439 \u0440\u0432\u0435\u043d\u0456\u0439 \u0433\u0440\u0438 \u043f\u043e\u0447\u0438\u043d\u0430\u045e\u0441\u044f \u0442\u0443\u0445!
    
Mobile Legends: Starts \u2013 \u0446\u0435 \u0431\u0456\u043b\u044c\u0448\u0435, \u043d\u0456\u0436\u0447\u0435 \u043f\u0440\u043e\u0441\u0442\u043e \u0431\u043e\u0442. \u0426\u0435 \u0442\u0432\u043e\u0454 \u043f\u043e\u043c\u0456\u0447\u0438\u043a, \u0442\u0440\u0435\u043d\u0435\u0440 \u0456 \u043f\u0440\u043e\u0432\u0456\u0434\u0438\u043d \u0443 \u0441\u0432\u0456\u0442\u0456 Mobile Legends. \u0413\u043e\u0442\u0443\u0439\u0441\u044f \u0434\u043e \u043d\u043e\u0432\u0438\u0445 \u043f\u0435\u0440\u0432\u043e\u043c\u0456\u0445 \u043f\u0435\u0440\u0432\u0435\u0432 \u0456\u0432\u0434\u0432\u0456\u0434\u0456\u043d\u043d\u0456\u0445 \u0432\u043d\u0438\u043c\u0430\u043d\u043d\u0456\u0439 \u0441\u0442\u0440\u0430\u043d\u044c\u043e\u0433\u043e \u0441\u043f\u0440\u0438\u0439\u043c\u0435\u043d\u0442\u0430 \u0456\u0437 \u043d\u0430\u0441\u0438\u043c\u0456!
    
\ud83d\ude80 <b>\u0420\u043e\u0437\u043f\u043e\u0447\u0430\u0442\u0438 \u043d\u0430\u0437\u0440\u0430\u0437 \u0456 \u0441\u0442\u0430\u043d\u044c \u043b\u0435\u0433\u0435\u0434\u043e\u0454!</b>
    """
)

# Призначення першої сторінки як привітального тексту
WELCOME_NEW_USER_TEXT = INTRO_PAGE_1_TEXT

# Кнопки для навігації в привітальному повідомленні
BUTTON_NEXT = "\u0414\u0430\u043b\u0438 \u27a1\ufe0f"
BUTTON_START = "\u0420\u043e\u0437\u043f\u043e\u0447\u0430\u0442\u0430\u0442\u0438 \ud83d\ude80"

# Головне меню
MAIN_MENU_TEXT = (
    """\ud83d\udc4b <b>\u0412\u0438\u0442\u0430\u0435\u043c\u0438, {user_first_name}, \u0443 Mobile Legends: Starts!</b>
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u043e\u0434\u043e\u0431\u0440\u0438\u0442\u044c \u043f\u043e\u0434\u0443\u0441\u043a\u043d\u044e \u043e\u043f\u0446\u0456\u0457 \u043d\u043e\u0436\u0435\u0432\u0435, \u0448\u0442\u043e \u0434\u043e\u0441\u043b\u0456\u0434\u0436\u0430\u0442\u0438 \u043c\u043e\u0436\u043b\u0438\u0432\u043e\u0441\u0442\u0456 \u0442\u0430 \u0432\u0434\u043e\u043a\u043e\u043d\u043e\u0432\u044f\u0442\u0438 \u0441\u0432\u043e\u0454 \u0456\u0433\u043e\u0432\u043e\u0433\u0438 \u0434\u043e\u0441\u0432\u0456\u0434\u0443.
    """
)

PROFILE_MENU_TEXT = (
    "\u0426\u0456 \u0442\u0435\u043a\u0441\u0442 \u0434\u043b\u044f \u043c\u0435\u043d\u044e \u043f\u0440\u043e\u0444\u0456\u043b\u044e. \u0417\u0430\u043c\u0456\u043d\u0456\u0442\u044c \u0456\u0433\u043e \u043d\u0430 \u043f\u043e\u0447\u0456\u043d\u043d\u0438\u0439 \u043a\u043e\u043d\u0442\u0435\u043d\u0442."
)

MAIN_MENU_DESCRIPTION = (
    """\ud83c\udfae <b>Mobile Legends: Starts \u0434\u043e\u043f\u043e\u043c\u043e\u0436\u0435 \u0432\u0443\u0430\u0441:</b>
\ud83c\udfc6 <b>\u041e\u0440\u0433\u0430\u043d\u0456\u0437\u0443\u0432\u0430\u0442\u0438 \u0442\u0443\u0440\u043d\u0456\u0440\u0438:</b> \u0421\u0442\u0432\u043e\u0440\u0438\u0442\u044c \u0432\u043e\u0441\u043e\u0432\u0438\u0445 \u0437\u0430\u043c\u0456\u043d\u043d\u044f, \u043a\u0435\u0440\u043c\u0443\u0439\u0442\u0438\u0442\u044c \u043c\u0438 \u0442\u0430 \u0437\u0430\u043f\u0438\u0441\u0443\u0439\u0442\u0438 \u0434\u0440\u0443\u0437\u0456\u0432 \u0432\u0438\u043f\u0456\u0440\u043e\u0431\u0438\u0442\u0438 \u0441\u0432\u043e\u0454\u0445 \u0441\u0443\u043b\u0438.
\ud83d\uddbc <b>\u0417\u0431\u0435\u0440\u0456\u0442\u0438 \u0441\u043a\u0440\u0456\u043d\u0448\u043e\u0442\u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0456\u0432:</b> \u0420\u043e\u0431\u0456\u0442\u044c \u0432\u0438\u0437\u0443\u0430\u043b\u044c\u043d\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438 \u043f\u0440\u043e \u0433\u0435\u0440\u043e\u0439\u0456\u0432, \u0437\u0431\u0435\u0440\u0456\u0442\u044c \u0432\u0433\u043e\u0432\u0430\u043d\u043d\u0456 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0457 \u0442\u0430 \u0434\u0438\u043b\u0438\u0442\u044c\u0441\u044f \u0437 \u043c\u0438\u043d\u0448\u0438\u043c\u0438 \u0433\u0440\u0430\u0432\u0446\u044f\u043c\u0438.
\ud83d\udcc8 <b>\u0412\u0456\u0434\u0441\u0442\u0430\u0436\u0443\u0432\u0430\u0442\u0438 \u0430\u043a\u0442\u0456\u0432\u043d\u0456\u0441\u0442\u044c:</b> \u041a\u043e\u043d\u0442\u0440\u043e\u043b\u044e\u0439\u0442\u044c \u0447\u0430\u0441\u0442\u043e\u0442\u044c \u0442\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u043c\u0430\u0442\u0447\u0456\u0432, \u0430\u043d\u0430\u043b\u0456\u0437\u0443\u0439\u0442\u0438 \u0441\u0432\u043e\u044e \u0433\u0440\u0443 \u0434\u043b\u044f \u0441\u0430\u0431\u0438\u043b\u0456\u0432\u043e\u0433\u043e \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0443.
\ud83e\udd47 <b>\u041e\u0442\u0440\u0438\u043c\u0443\u0432\u0430\u0442\u0438 \u0434\u043e\u0441\u0438\u0433\u043d\u0435\u043d\u043d\u044f:</b> \u0417\u0434\u043e\u0431\u0430\u0442\u044c\u0442\u044f \u0432\u0438\u043d\u0430\u0442\u0440\u043e\u0432\u0430\u0434\u044b \u0437\u0430 \u0432\u0430\u0448\u0456 \u0437\u0443\u0441\u0443\u043b\u0438, \u044f\u043a\u0456 \u0437\u0430\u0441\u0432\u0456\u0442\u0436\u0443\u044e\u0442\u044c \u0432\u0430\u0448\u0438 \u0440\u043e\u0437\u0432\u0438\u0442\u043a\u0443 \u0442\u0430 \u043c\u0430\u0439\u0441\u0442\u0435\u0440\u043d\u0456\u0441\u044c \u0443 \u0433\u0440\u0435\u0438.
    """
)

MAIN_MENU_ERROR_TEXT = (
    """\u2757\ufe0f <b>\u0421\u0442\u0430\u043b\u0430 \u043f\u043e\u043c\u0438\u043b\u043a\u0430.</b>
\u0411\u0443\u0434\u044c \u043b\u0430\u0441\u043f\u0430, \u0441\u043f\u043e\u0442\u0440\u0438\u0431\u0443\u0439\u0442\u0435 \u0449\u0435 \u0434\u0430\u0436 \u0440\u0430\u0437 \u043e\u0440\u0430 \u043f\u043e\u0432\u0456\u0440\u043d\u044e\u0442\u044c\u0441\u044f \u0434\u043e \u0433\u043e\u043b\u043e\u0432\u043d\u043e\u0433\u043e \u043c\u0435\u043d\u044e. \u0423\u0441\u043b\u0438 \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u0430 \u043d\u0435 \u0437\u043c\u0438\u043d\u045b\u0442\u0435, \u0437\u0432\u0435\u0440\u043d\u044e\u0442\u044c\u0441\u044f \u0434\u043e \u043f\u043e\u0434\u043f\u0456\u0440\u0442\u0438."""
)

MAIN_MENU_BACK_TO_PROFILE_TEXT = (
    """\ud83d\udd19 \u041f\u043e\u0432\u0456\u0440\u043d\u0435\u043d\u043d\u044f \u0434\u043e <b>\u201c\u041c\u0456\u0439 \u041f\u0440\u043e\u0444\u0456\u043b\u044c\u201d</b>.
    """
)

# Меню навігації
NAVIGATION_MENU_TEXT = (
    """\ud83e\udd2e <b>\u041d\u0430\u0432\u0456\u0433\u0430\u0446\u0456\u044f</b>
\u041e\u0431\u0456\u0440\u0435\u0447 \u0440\u043e\u0437\u0440\u0456\u0434: \u0433\u0435\u0440\u043e\u0439\u0438, \u0433\u0430\u0439\u0434\u0438, \u0431\u0438\u043b\u0434\u0438, \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438 \u0456 \u0433\u043e\u043b\u043e\u0441\u0443\u0432\u0430\u043d\u043d\u044f.
    """
)

NAVIGATION_INTERACTIVE_TEXT = (
    """\ud83e\udd2e <b>\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u0456 \u0440\u043e\u0437\u0440\u0456\u0434\u0438:</b>
\ud83e\udd8a <b>\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0456:</b> \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f \u043f\u0440\u043e \u0433\u0435\u0440\u0456\u0439\u0456\u0432, \u0456\u0445 \u0437\u0434\u0456\u0431\u043d\u0430\u0441\u0442\u0456 \u0442\u0430 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454.
\ud83d\udcda <b>\u0413\u0430\u0439\u0434\u0438:</b> \u0442\u0430\u043a\u0442\u0438\u0447\u043d\u0456 \u043f\u043e\u0432\u0430\u0434\u0438 \u0434\u043b\u044f \u0440\u0456\u0437\u043d\u0438\u0445 \u0435\u0442\u0430\u043f\u0456\u0432 \u0433\u0440\u0438.
\ud83d\udd27 <b>\u0411\u0438\u043b\u0434\u0438:</b> \u0441\u0442\u0432\u043e\u0440\u0435\u043d\u043d\u044f \u0442\u0430 \u043d\u0430\u043b\u044c\u043a\u0430\u0437\u0443\u0432\u0430\u043d\u043d\u044f \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f.
\u2696\ufe0f <b>\u041a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438:</b> \u0454\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0430 \u043f\u0440\u043e\u0442\u0438\u0434\u0456\u045a\u0430 \u0441\u043a\u043e\u043b\u043e\u0434\u043d\u0456\u0445 \u0433\u0435\u0440\u0456\u0459 \u0441\u0443\u043f\u043e\u0440\u0456\u0442\u0438\u0432\u043d\u043e\u0433\u043e \u0441\u0443\u043f\u043e\u0440\u0456\u0432\u043d\u0438\u043a\u0443.
\ud83d\udcc8 <b>\u0413\u043e\u043b\u043e\u0441\u0443\u0432\u0430\u043d\u043d\u044f:</b> \u0431\u0435\u0440\u0456\u0442\u044c \u0443\u0441\u0442\u0430\u043f\u0443\u0447 \u0432 \u043e\u043f\u0438\u0442\u0443\u0432\u0430\u043d\u043d\u044f\u0445, \u0432\u043f\u043b\u0438\u0432\u0430\u044f\u0442\u0438 \u043d\u0430 \u0432\u0438\u0434\u043e\u0432\u0442\u0430\u043d\u043d\u044f \u0441\u0432\u0435\u0440\u043e\u0431\u0443.
\ud83d\udd25 <b>META:</b> \u0430\u043d\u0430\u043b\u0456\u0437 \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0438\u0445 \u0442\u0435\u043d\u0434\u0435\u043d\u0446\u0456\u0439 \u0433\u0440\u0438.
\ud83c\udfc6 <b>M6:</b> \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u044c\u043d\u0456 \u043f\u043e\u0434\u0456\u044f\u0442\u0438 \u0442\u0430 \u043d\u0430\u0433\u043e\u0440\u043e\u0434\u0430\u044f.
\ud83d\udc79 <b>GPT:</b> AI \u043f\u043e\u0434\u043f\u0456\u0440\u0433\u0430 \u0442\u0430 \u0432\u043e\u0434\u043f\u0456\u0432\u0438\u0434\u0438 \u043d\u0430 \u0432\u0430\u0448\u0456 \u0437\u0430\u043f\u0438\u0442\u0430\u043d\u043d\u044f.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043a\u0430\u043f\u0430\u0442\u0443\u0440\u0456\u044e, \u0448\u0442\u043e\u0431\u0443 \u043f\u0435\u0440\u0435\u0433\u043b\u044f\u0434\u0438\u0442\u0438 \u0441\u043f\u0438\u0441\u043e\u043a \u0433\u0435\u0440\u043e\u0459.
    """
)

# Меню персонажів
HEROES_MENU_TEXT = (
    """\ud83e\udd8a <b>\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0456</b>
\u041e\u0431\u0456\u0440\u0435\u0447 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u044e \u0433\u0435\u0440\u043e\u0459, \u0448\u0442\u043e\u0431\u0443 \u0434\u0438\u0437\u043d\u0430\u0439\u043d\u044f \u043f\u0440\u043e \u0456\u0445\u043d\u0456 \u043c\u043e\u0436\u043d\u043e\u0441\u0442\u0456 \u0442\u0430 \u0440\u043e\u0437\u0440\u0430\u0431\u043e\u0442\u0443\u0432\u0430\u0442\u0438 \u0435\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0456 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454.
    """
)

HEROES_INTERACTIVE_TEXT = (
    """\ud83d\udcce <b>\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0454 \u0433\u0435\u0440\u043e\u0459:</b>
\ud83d\udee1\ufe0f <b>\u0422\u0430\u043d\u043a:</b> \u043c\u0456\u0446\u043d\u0456 \u0433\u0435\u0440\u043e\u0439\u0438 \u0434\u043b\u044f \u0437\u0430\u0445\u043e\u0434\u0443 \u043a\u043e\u043c\u0430\u043d\u0434\u0438.
\ud83e\udd9c\ud83c\udffb <b>\u041c\u0430\u0433:</b> \u0437\u0430\u0432\u0434\u0430\u044e\u0442\u044c \u043c\u0430\u0433\u0456\u0447\u043d\u0456\u044e \u0448\u043a\u043e\u0434\u0443 \u0442\u0430 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044e\u044e\u0442\u044c \u0445\u0456\u0434 \u0431\u043e\u044e.
\ud83c\udf0b <b>\u0421\u0442\u0440\u0438\u043b\u0435\u0446\u044c:</b> \u0441\u0442\u0430\u0431\u0456\u043b\u044c\u043d\u0430 \u0448\u043a\u043e\u0434\u0430 \u0437 \u0434\u0438\u0441\u0442\u0430\u043d\u0446\u0456.
\u2694\ufe0f <b>\u0410\u0441\u0430\u0441\u0456\u043d:</b> \u0448\u0432\u0456\u0434\u043a\u0456 \u0430\u0442\u0430\u043a\u0438 \u043f\u043e \u043a\u043b\u044e\u0447\u0456\u0432\u0438\u043c \u0437\u0430\u0445\u043e\u043b\u044c.
\2764\ufe0f <b>\u041f\u0438\u0434\u0442\u043e\u0440\u0436\u043a\u0430:</b> \u043b\u0443\u0447\u0435\u043d\u043d\u044f \u0442\u0430 \u043f\u043e\u0441\u0438\u043b\u0435\u043d\u043d\u044f \u0441\u0430\u043b\u0456\u0437\u043d\u0456\u043a\u0438\u0432.
\ud83e\uddd1 <b>\u0411\u043e\u044e\u0454:</b> \u0437\u0431\u0430\u043b\u0430\u043d\u0441\u043e\u0432\u0430\u043d\u0456 \u0433\u0435\u0440\u043e\u0439\u0438 \u0437 \u0430\u0442\u0430\u043a\u043e\u044e \u0456 \u0437\u0430\u0445\u043e\u0434\u043e\u043c.
\ud83d\udd25 <b>META:</b> \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0456 \u0442\u0435\u043d\u0434\u0435\u043d\u0446\u0456\u0439 \u0433\u0440\u0438.
\ud83c\udfc6 <b>M6:</b> \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u044c\u043d\u0456 \u043f\u043e\u0434\u0456\u044f\u0442\u0438 \u0442\u0430 \u043d\u0430\u0433\u043e\u0440\u043e\u0434\u0430\u044f.
\ud83d\udc79 <b>GPT:</b> AI \u043f\u043e\u0434\u043f\u0456\u0440\u0433\u0430 \u0442\u0430 \u0432\u043e\u0434\u043f\u0456\u0432\u0438\u0434\u0438 \u043d\u0430 \u0432\u0430\u0448\u0456 \u0437\u0430\u043f\u0438\u0442\u0430\u043d\u043d\u044f.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043a\u0430\u043f\u0430\u0442\u0443\u0440\u0456\u044e, \u0448\u0442\u043e\u0431\u0443 \u043f\u0435\u0440\u0435\u0433\u043b\u044f\u0434\u0438\u0442\u0438 \u0441\u043f\u0438\u0441\u043e\u043a \u0433\u0435\u0440\u043e\u0459.
    """
)

# Меню класу героїв
HERO_CLASS_MENU_TEXT = (
    """\u0412\u0438\u0431\u0435\u0440\u0438\u0442\u044c \u0433\u0435\u0440\u043e\u044f \u0437 \u043a\u043b\u0430\u0441\u0443 <b>{hero_class}</b> \u0434\u043b\u044f \u0434\u043e\u043a\u043b\u0430\u0434\u043d\u0452 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u0454 \u043f\u0440\u043e \u0437\u0434\u0438\u0431\u043d\u0430\u0441\u0442\u0456, \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454 \u0442\u0430 \u0431\u0438\u043b\u0434\u0438."""
)

HERO_CLASS_INTERACTIVE_TEXT = (
    """\ud83d\udcdd <b>\u0413\u0435\u0440\u043e\u0439\u0456 \u043a\u043b\u0430\u0441\u0443 {hero_class}:</b>
\u0421\u043b\u0438\u0441\u043e\u043a \u0433\u0435\u0440\u043e\u0459\u0456\u0432 \u0446\u0456\u0445 \u043a\u043b\u0430\u0441\u0443. \u041e\u0431\u0456\u0440\u0435\u0447 \u0433\u0435\u0440\u043e\u044f \u0434\u043b\u044f \u0434\u0435\u0442\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043e\u043f\u0438\u0441\u0443.
    """
)

# Меню гайдів
GUIDES_MENU_TEXT = (
    """\ud83d\udcdc <b>\u0413\u0430\u0439\u0434\u0438</b>
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u043e\u0434\u043e\u0431\u0440\u0438\u0442\u044c \u043f\u043e\u0434\u0440\u0435\u0437\u0434 \u0433\u0430\u0439\u0434\u0456\u0432 \u0434\u043b\u044f \u0432\u0456\u0432\u0447\u0443\u0432\u0430\u043d\u043d\u044f \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454, \u0442\u0430\u043a\u0442\u0456\u043a \u0442\u0438 \u043f\u043e\u0434\u0430\u0440\u045b.
    """
)

GUIDES_INTERACTIVE_TEXT = (
    """\ud83d\udcd5 <b>\u041f\u0456\u0434\u0440\u043e\u0437\u0434\u0456\u043b\u044b \u0433\u0430\u0439\u0434\u0456\u0432:</b>
\ud83c\udf1a <b>\u041d\u043e\u0432\u0456 \u0413\u0430\u0439\u0434\u0438:</b> \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0456 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0438 \u0437\u0430 \u043e\u0441\u043b\u0435\u0434\u043d\u0438\u043c\u0438 \u0442\u0435\u043d\u0434\u0435\u043d\u0446\u0456\u0439\u0430\u043c\u0438.
\ud83c\udf1f <b>\u0422\u043e\u043f \u0413\u0430\u0439\u0434\u0438:</b> \u043d\u0430\u0439\u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u0456\u0448\u0456 \u0433\u0430\u0439\u0434\u0438, \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u0435\u043d\u0456 \u0441\u043f\u0456\u043b\u044c\u043d\u043e\u0442\u043e\u0439\u044e.
\ud83d\udcda <b>\u0414\u043b\u044f \u041f\u043e\u0447\u0430\u0442\u043a\u0456\u0432\u043d\u0456\u0445:</b> \u0431\u0430\u0437\u0456 \u0456\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0456\u044e \u0434\u043b\u044f \u043d\u043e\u0432\u0438\u0445 \u0433\u0440\u0430\u0432\u0446\u0456\u0432.
\ud83e\udd9d <b>\u0421\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454 \u0433\u0440\u0438:</b> \u043f\u043e\u0433\u0440\u0443\u0431\u0456\u0434\u0435\u043d\u045b \u0442\u0430\u043a\u0442\u0438\u0447\u043d\u0456 \u043f\u043e\u0432\u0430\u0434\u0438.
\ud83e\udd1d <b>\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430 \u0413\u0440\u0430:</b> \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0438 \u043f\u0440\u043e \u0454\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0456 \u0432\u0430\u0437\u044f\u0447\u043d\u0456\u044e \u0432\u0432\u0430\u044f\u043c\u043e\u0434\u043d\u0456\u044e \u0443 \u043a\u043e\u043c\u0430\u043d\u0434\u0456.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u0456\u0434\u0440\u043e\u0437\u0434\u0456\u043b \u0433\u0430\u0439\u0434\u0456\u0432, \u0448\u0442\u043e\u0431\u0443 \u043e\u0442\u043c\u0438\u0442\u044c \u043a\u043e\u0440\u0443\u0441\u043d\u0443 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044e \u0442\u0430 \u0437\u0430\u0441\u0442\u0430\u043d\u0443\u0432\u0430\u0442\u0438 \u0456\u0433\u043e \u043d\u0430 \u043f\u0440\u0430\u0446\u0456\u0447\u0456.
    """
)

NEW_GUIDES_TEXT = (
    """\ud83d\udcc4 <b>\u041d\u043e\u0432\u0456 \u0433\u0430\u0439\u0434\u0438:</b>
\u0421\u043b\u0438\u0441\u043e\u043a \u043d\u043e\u0432\u0456\u0445 \u0433\u0430\u0439\u0434\u0456\u0432 \u043d\u0430\u0440\u0430\u0437\u0438 \u0432\u0456\u0441\u0442\u0443\u044f\u043d\u0438. \u041d\u0435\u0437\u0430\u0431\u0430\u0440\u043e\u043d \u043c\u0438 \u0434\u043e\u0434\u0430\u043c\u043e \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u045b \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0438, \u044f\u043a\u0438 \u0432\u043e\u044f\u0437\u0434\u0456\u043c\u0430\u044e\u0442\u044c \u043d\u0430\u0439\u0441\u0432\u0456\u0436\u0456\u043c \u0442\u0440\u0435\u043d\u0434\u0430\u043c \u0433\u0440\u0438.
    """
)

POPULAR_GUIDES_TEXT = (
    """\ud83c\udf31 <b>\u0422\u043e\u043f \u0413\u0430\u0439\u0434\u0438:</b>
\u041f\u043e\u043a\u0438 \u043d\u0435\u043c\u0430 \u0441\u043f\u0438\u0441\u043e\u043a \u043d\u0430\u0439\u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u0456\u0445 \u0433\u0430\u0439\u0434\u0456\u0432. \u0417\u0430\u043b\u0438\u0448\u0430\u044f\u0442\u0441\u044f \u0437 \u043c\u0438\u043d\u0430\u043c\u0438 – \u043d\u0435\u0437\u0430\u0431\u0430\u0440\u043e\u043d \u0432\u0443\u0441\u0435 \u0437 \u043d\u0430\u0439\u0446\u0456\u043d\u043d\u045b\u043c\u0438 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430\u043c\u0438, \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u0435\u043d\u0438\u043c\u0438 \u0441\u043f\u0456\u043b\u044c\u043d\u043e\u0442\u043e\u0439\u044e \u0441\u043f\u0456\u043b\u044c\u043d\u043e\u0442\u043e\u044c.
    """
)

BEGINNER_GUIDES_TEXT = (
    """\ud83d\udcda <b>\u0413\u0430\u0439\u0434\u0438 \u0434\u043b\u044f \u041f\u043e\u0447\u0430\u0442\u043a\u0456\u0432\u043d\u0456\u0445:</b>
\u0421\u043a\u043e\u0440\u043e \u0442\u0438\u0434\u0443\u0442\u044c\u0441\u044f \u0433\u0430\u0439\u0434\u0438, \u044f\u043a\u0438 \u0434\u043e\u043f\u043e\u043c\u043e\u0436\u0443\u0442\u044c \u043d\u043e\u0432\u0430\u0447\u043a\u0430\u043c \u0448\u044c\u0442\u043e\u043f\u0430\u0447\u0443\u0442\u044c\u044c \u043e\u0441\u043d\u043e\u0432\u0438 \u0433\u0440\u0438, \u0437\u0440\u043e\u0437\u0443\u043c\u0438\u0442\u0438 \u0433\u043e\u043b\u043e\u0432\u043d\u0456 \u043c\u0435\u0445\u0430\u043d\u0456\u043a\u0438 \u0442\u0430 \u0432\u043e\u0440\u0438\u0431\u0438\u0442\u0438 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u044e \u0434\u043b\u044f \u0443\u0441\u043f\u0456\u0448\u043d\u043e\u0433\u043e \u0441\u0442\u0430\u0440\u0442\u0443.
    """
)

ADVANCED_TECHNIQUES_TEXT = (
    """\ud83e\udd9d <b>\u0421\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454 \u0433\u0440\u0438:</b>
\u0423 \u0446\u0435\u043c\u0443 \u0440\u043e\u0437\u0444\u0435\u043b\u0456 \u0437\u044f\u0432\u0438\u0442\u044c\u0441\u044f \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0438 \u0434\u043b\u044f \u0434\u043e\u0441\u0451\u0434\u0447\u0435\u043d\u043d\u0438\u0445 \u0433\u0440\u0430\u0432\u0446\u0456\u0432, \u0456\u043a\u0456 \u043f\u0440\u043e\u044f\u0433\u0443\u0442\u044c \u043f\u043e\u0433\u0440\u0443\u0431\u0438\u0442\u044c \u0441\u0432\u0456\u0439\u0456 \u043d\u043e\u0432\u0438\u044f \u0437\u043d\u0430\u043d\u0438\u044f, \u0432\u043e\u0442\u0448\u043b\u0438\u0444\u044e\u0442\u044c \u0442\u0430\u043a\u0442\u0438\u043a\u0443 \u0442\u0430 \u0434\u043e\u0433\u043e\u0447\u0438\u0442\u044c \u0441\u043f\u0440\u0430\u0432\u043d\u0438\u0441\u044c\u044e.
    """
)

TEAMPLAY_GUIDES_TEXT = (
    """\ud83e\udd1d <b>\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430 \u0413\u0440\u0430:</b>
\u041d\u0435\u0437\u0430\u0431\u0430\u0440\u043e\u043d \u0442\u0438\u0445 \u0431\u0443\u0434\u044c \u0433\u0430\u0439\u0434\u0438, \u0441\u0442\u043e\u044f\u0442\u044c \u0433\u0430\u0439\u0434\u0438, \u0441\u0442\u0440\u0430\u0442\u0438\u044f\u0442\u044c \u0432\u0430\u0441 \u0456\u0432\u0456\u0434\u0435\u0442\u044c \u0435\u0441\u0442\u044c\u0456\u0447\u043d\u0456 \u0432\u0430\u0432\u0438\u0432\u043d\u0456\u044e \u0432\u0432\u0430\u0439\u043c\u043e\u0434\u044f \u0437 \u043a\u043e\u043c\u0430\u043d\u0434\u043e\u044e, \u0440\u043e\u0437\u0434\u0456\u043b\u044e\u0432\u0443\u0442\u044c \u0440\u043e\u043b\u0456, \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0446\u044e\u0432\u044c \u0442\u0430 \u043f\u043b\u0430\u043d\u0443\u0432\u0430\u043d\u043d\u044f \u0441\u043f\u043e\u043b\u0456\u0434\u043d\u044c\u043e\u0433\u0438 \u0434\u0456\u0439.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u0456\u0434\u0440\u043e\u0437\u0434\u0456\u043b \u0433\u0430\u0439\u0434\u0456\u0432, \u0448\u0442\u043e\u0431\u0443 \u043e\u0442\u0446\u0435\u043d\u0438\u0442\u044c \u0432\u043e\u043b\u044c\u0448\u0438\u0432\u0438 \u0441\u0443\u0448\u043e\u043a\u0456\u0441\u0442\u044f \u0441\u0442\u0430\u043d\u043e\u0432\u044f\u044e \u043e\u0432\u0435\u0441\u043d\u0456\u0445 \u0440\u0456\u0448\u0435\u043d\u043d\u045b\u0445 \u043f\u0440\u0438\u043c\u0456\u0435\u043a, \u044f\u043a\u0456 \u0440\u0435\u0433\u0443\u043b\u044f\u0440\u043d\u0438 \u0432\u0438\u0441\u043e\u0441\u0448\u0438\u0432\u0456 \u0434\u043e\u0441\u043f\u0456\u0437\u0435\u043d\u0438\u045b \u0433\u0440\u0430\u0432\u0446\u0456\u0432.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u043e\u0434\u0440\u0435\u0434\u043b\u044f\u0432, \u0448\u0442\u043e\u0431\u0443 \u043f\u043e\u043a\u0440\u0435\u043f\u0440\u0438\u0441\u0442\u0438 \u0441\u043f\u0438\u0441\u043e\u043a \u0433\u0435\u0440\u043e\u0459\u0456\u0432.
    """
)

# Меню контр-піків
COUNTER_PICKS_MENU_TEXT = (
    """\u2696\ufe0f <b>\u041a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438</b>
\u041e\u0431\u0456\u0440\u0435\u0447 \u043e\u043f\u0446\u0456\u0457 \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u0433\u043b\u044f\u0434\u0443 \u043e\u0440\u0443 \u0441\u0442\u0432\u043e\u0440\u0438\u0442\u044c \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438.
    """
)

COUNTER_PICKS_INTERACTIVE_TEXT = (
    """\ud83d\udc75\ud83c\udffb <b>\u041a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438:</b>
\ud83d\udd0e <b>\u041f\u0435\u0440\u0435\u0433\u043b\u044f\u0434\u0443\u0442\u044c \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438:</b> \u043e\u0442\u0440\u0438\u043c\u0443\u0442\u0435 \u0441\u043f\u0438\u0441\u043e\u043a \u0433\u0435\u0440\u043e\u0459\u0456\u0432, \u044f\u043a\u0456 \u0435\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u043e \u043f\u0440\u043e\u0442\u0438\u0434\u0456\u044e\u0442\u044c \u0432\u0456\u0431\u0430\u0440\u0430\u043d\u043e\u0433\u043e \u0441\u0443\u043f\u0440\u043e\u0432\u043e\u0442\u043d\u0438\u043a\u0443.
\ud83d\udc4d <b>\u0421\u0442\u0432\u043e\u0440\u0438\u0442\u044c \u0432\u043e\u043f\u043e\u043b\u0435\u043d\u0438\u0439 \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a:</b> \u0437\u0430\u043f\u0440\u043e\u043f\u043e\u0437\u0443\u0439\u0442\u044c \u0432\u043e\u043f\u043e\u043b\u0435\u043d\u0438\u0439 \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a, \u0437\u0430\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0439 \u043d\u0430 \u0432\u0430\u0448\u043e\u043c\u0443 \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0438\u0438.
\ud83d\udd25 <b>\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u0456 \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0438:</b> \u043e\u0437\u043d\u0430\u043c\u043e\u0446\u044f\u0441\u044f \u0437 \u043d\u0430\u0439\u0443\u0441\u043f\u0456\u0448\u043d\u0456\u0448\u0438\u043c\u0438 \u043f\u0440\u0438\u043a\u0430\u0437\u0430\u043c\u0438, \u044f\u043a\u0456 \u0440\u0435\u0433\u0443\u043b\u044c\u043d\u043e \u0432\u0438\u0441\u043e\u0441\u0448\u0438\u0432\u0456 \u0434\u043e\u0441\u043f\u0456\u0437\u0435\u043d\u0456 \u0433\u0440\u0430\u0432\u0446\u0456\u0432\u0438.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043f\u043e\u0434\u0443\u0445\u043d\u044e \u0434\u043e\u0431\u0440\u0456 \u0434\u0438\u0430\u043b\u044c\u043d\u0443 \u0434\u0456\u0439, \u0448\u0442\u043e\u0431\u0443 \u043f\u043e\u043a\u0440\u0435\u043f\u0440\u043e\u0432\u0438\u0442\u044c\u0438 \u0432\u0438\u0448\u0430\u043d\u0438 \u043d\u0430 \u043f\u0435\u0440\u0435\u0432\u043e\u0433\u0443 \u043f\u0435\u0440\u0432\u0435\u0433\u043e \u043f\u043e\u0441\u0442\u0443\u043c\u043a\u0443.
    """
)

COUNTER_SEARCH_TEXT = "\ud83d\udd0e \u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0456\u043c\u044f \u0433\u0435\u0440\u043e\u044f, \u043f\u0440\u043e\u0442\u0438 \u044f \u0432\u044b\u0445\u043e\u0434\u0443 \u0444\u0443\u043d\u043a\u0446\u0456\u0457 \u044f \u0448\u0443\u043a\u0430\u0458\u0435\u0442\u044c \u0456\u043c\u044f \u0433\u0435\u0440\u043e\u044f, \u043f\u0440\u043e\u0442\u0438 \u043a\u0443\u0432 \u044f \u0448\u0443\u043a\u0430\u0458\u0435\u0442\u044c \u0435\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0438\u0439 \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a:"

COUNTER_LIST_TEXT = (
    """\ud83d\udcc3 <b>\u0421\u043f\u0438\u0441\u043e\u043a \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0456\u0432:</b>
\u041f\u043e\u043a\u0438 \u0441\u0442\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f \u043f\u0440\u043e \u043a\u043e\u043d\u0442\u0440-\u043f\u0456\u043a\u0456 \u0434\u043b\u044f \u043e\u0431\u0430\u0440\u0430\u043d\u043e\u0433\u043e \u0433\u0435\u0440\u043e\u0459\u0430 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u044f\u043d\u0430. \u0421\u043b\u0435\u0434\u043a\u0443\u044e\u0442\u0438 \u0437\u0430 \u043e\u043d\u043e\u0432\u0443\u0432\u0430\u043d\u0438\u044f\u043c\u0438 \u2014 \u043d\u0435\u0437\u0430\u0431\u043e\u0439\u043d\u043e \u044f \u0437\u0430\u0431\u0443\u0434\u0435\u0442\u044c\u0441\u044f \u0432 \u0443\u0441\u0442\u0430\u043f\u0443\u0447\u043d\u0430\u0445 \u2014 \u043d\u0435\u0437\u0430\u0431\u043e\u0439\u043d\u043e \u044f \u043e\u0442\u0440\u0438\u043c\u0443\u0442\u044c \u043f\u043e\u0432\u043d\u0438\u043d\u043d\u0456\u0439 \u0441\u043f\u0438\u0441\u043e\u043a \u043c\u043e\u0436\u043b\u0438\u0432\u0456\u0445 \u0440\u0456\u0448\u0435\u043d\u043d\u044f\u0445.
    """
)

# Меню білдів
BUILDS_MENU_TEXT = (
    """\u1f6e1\ufe0f <b>\u0411\u0438\u043b\u0434\u0438</b>
\u0422\u0443\u0445 \u0432\u0438 \u043c\u043e\u0436\u043d\u0435\u0442\u0435 \u0441\u0442\u0432\u043e\u0440\u0438\u0442\u044c \u043d\u043e\u0432\u0456\u0445 \u0431\u0438\u043b\u0434\u0456\u0432, \u043f\u0435\u0440\u0435\u0433\u043b\u044f\u0434\u0430\u0442\u044c \u0441\u0432\u043e\u0438\u0445 \u0437\u0431\u0435\u0434\u0435\u043d\u043d\u044b\u0445 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0456\u0432 \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f \u0432\u0430\u0440\u0456\u0430\u043d\u0442\u043e\u0432.
    """
)

BUILDS_INTERACTIVE_TEXT = (
    """\ud83d\udd27 <b>\u041e\u043f\u0446\u0456\u045e \u0431\u0438\u043b\u0434\u0456\u0432:</b>
\ud83d\udec3\ufe0f <b>\u0421\u0442\u0432\u043e\u0440\u0438\u0442\u044c \u043d\u043e\u0432\u0438\u0439 \u0431\u0438\u043b\u0434:</b> \u0430\u0434\u0430\u043f\u0442\u0443\u0439\u0442\u0435 \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f \u043f\u0443\u0434 \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0433\u043e \u0433\u0435\u0440\u043e\u044f, \u0432\u0443\u0447\u0430\u043b\u044f\u0447\u0438 \u0456\u0457 \u0437\u0430\u0433\u043b\u0456\u0441\u043d\u0456 \u0442\u0430 \u0441\u0443\u0442\u0430\u0446\u0456\u0457, \u0430 \u0442\u0430\u043a\u0438\u043c \u0447\u0438\u043c \u0434\u043e\u0433\u0443\u0434\u044f\u0442\u0438 \u043a\u0440\u0435\u0448\u0438\u0432\u0438\u0445 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0456\u0432.
\ud83d\udd25 <b>\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u0456 \u0431\u0438\u043b\u0434\u0438:</b> \u0434\u0438\u0437\u043d\u0430\u0439\u0442\u0435 \u043f\u043e\u0440\u044f\u0434\u043a\u0443, \u044f\u043a\u0456 \u043e\u0442\u0442\u0440\u0438\u043c\u0443\u0442\u0435 \u043e\u0442\u043a\u0443\u0434\u043d\u0456\u0445 \u0431\u0438\u043b\u0434\u0456\u0432, \u0442\u0430 \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u043a\u0430\u0442\u0435\u0441\u044c \u0456\u0445 \u043d\u0430 \u0432\u043e\u043b\u043e\u0448\u0456\u0431\u0443\u0434\u043d\u044f \u0443 \u0441\u043f\u0456\u043b\u044c\u043d\u043e\u0442\u043e\u0439\u0443.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043e\u043f\u0446\u0456\u045e, \u0448\u0442\u043e\u0431\u0443 \u0434\u043e\u0437\u0431\u0438\u0442\u044c \u0432\u0430\u0448 \u0430\u0440\u0435\u0441\u043d\u0430\u043b \u0441\u043f\u043e\u0440\u044f\u0434\u043a\u0443 \u043c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e \u0435\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0438\u043c \u0430\u0440\u0441\u0435\u043d\u0430\u043b\u044c\u043c \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f.
\u041e\u0431\u0456\u0440\u0435\u0447 \u043e\u043f\u0446\u0456\u045e, \u0448\u0442\u043e\u0431\u0443 \u0437\u0430\u043c\u0430\u0437\u0443\u0432\u0430\u0442\u0438 \u0432\u0430\u0448 \u0430\u0440\u0441\u0435\u043d\u0430\u043b \u0441\u043f\u043e\u0440\u044f\u0434\u043a\u0443 \u043c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e \u0435\u0444\u0435\u043a\u0442\u0456\u0432\u043d\u0438\u043c \u0430\u0440\u0441\u0435\u043d\u0430\u043b\u044c\u043c \u0441\u043f\u043e\u0440\u044f\u0434\u0436\u0435\u043d\u043d\u044f.
    """
)

COUNTER_SEARCH_RESPONSE_TEXT = (
    """\ud83d\udd0e \u0412\u0438 \u0448\u0443\u043a\u0430\u0458\u0435\u0442\u044c \u0433\u0435\u0440\u043e\u044f: <i>{hero_name}</i>.
\u041f\u043e\u0448\u0443\u043a \u0433\u0435\u0440\u043e\u044f \u043f\u043e\u043a\u043e \u043d\u0435\u0442\u043e\u043f\u043e\u0434\u0456\u0434\u0434\u0430\u0432\u044f\u0442\u044c\u0441\u044f. \u0423 \u043c\u0430\u0439\u0443\u0442\u043d\u0452\u043c \u0432\u0443\u0430\u043c \u0437\u0430\u043c\u043e\u0436\u0435\u0442\u0435 \u043e\u0442\u0440\u0438\u043c\u0443\u0442\u044c \u0434\u0435\u0442\u0430\u043b\u0452 \u0434\u0430\u043d\u0452 \u043f\u0440\u043e \u0431\u0443\u0434\u044c-\u0430\u0442\u043f\u043e\u0440\u0430\u043d\u043e\u0433\u043e \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430, \u0432\u043a\u0443\u043b\u044f\u0447\u0443\u044e\u0447\u0438 \u0456\u0445 \u0437\u0434\u0438\u0431\u043d\u0430\u0441\u0442\u0456, \u0431\u0438\u043b\u0434\u0438 \u0442\u0430 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0456\u0454 \u0432\u0438\u0434\u043f\u043e\u0432\u0438\u0434\u0430\u043d\u043d\u044f.
    """
)

# Інші тексти збережені в оригінальному форматі.
# Покращення можна адаптувати до будь-яких змін за вашим запитом.
