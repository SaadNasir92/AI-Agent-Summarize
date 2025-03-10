import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_text(content):
    """Calls OpenAI's GPT to summarize text."""
    if not openai.api_key:
        raise ValueError("Missing OpenAI API key. Set it in the .env file.")

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following text in a concise and structured way.",
            },
            {"role": "user", "content": content},
        ],
    )

    return response["choices"][0]["message"]["content"]
