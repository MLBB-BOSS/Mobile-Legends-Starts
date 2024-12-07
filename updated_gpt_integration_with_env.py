
import openai
import os

# Load API key and API URL
openai.api_key = os.getenv('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"  # Ensure this matches your environment

def get_gpt_response(prompt, model="gpt-3.5-turbo"):
    """Send a request to the OpenAI API to get a response."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base=API_URL  # Use the specified API URL
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
