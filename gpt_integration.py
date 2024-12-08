# gpt_integration.py

import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def get_gpt_response(question: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(OPENAI_API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data['choices'][0]['message']['content'].strip()
                    return answer
                else:
                    logger.error(f"GPT API Error: {response.status} - {await response.text()}")
                    return "Виникла помилка при обробці вашого запитання. Спробуйте пізніше."
        except Exception as e:
            logger.error(f"Exception during GPT API call: {e}")
            return "Виникла помилка при обробці вашого запитання. Спробуйте пізніше."
