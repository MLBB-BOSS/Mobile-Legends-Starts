# gpt_integration.py

import openai
from config import settings
import logging

logger = logging.getLogger(__name__)

async def get_gpt_response(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        logger.error(f"Помилка при отриманні відповіді від GPT: {e}")
        return "Вибачте, виникла помилка при обробці вашого запитання."