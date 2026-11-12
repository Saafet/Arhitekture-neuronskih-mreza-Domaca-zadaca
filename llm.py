import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS

load_dotenv()  # učita DEEPSEEK_API_KEY iz datoteke .env

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

MODEL = "deepseek-flash"  # ako agent često griješi, probajte "deepseek-v4-pro"


def pitaj_model(messages):
    """Pošalje razgovor i opise alata modelu i vrati njegovu poruku."""
    odgovor = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        max_tokens=300,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return odgovor.choices[0].message