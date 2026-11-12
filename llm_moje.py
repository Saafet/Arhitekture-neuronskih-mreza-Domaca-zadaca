import os

from dotenv import load_dotenv
from openai import OpenAI

from tools_moje import TOOLS

load_dotenv()  # učita DEEPSEEK_API_KEY iz datoteke .env

KLJUC = os.getenv("DEEPSEEK_API_KEY")
if not KLJUC:
    raise SystemExit("Nedostaje DEEPSEEK_API_KEY u datoteci .env")

klijent = OpenAI(api_key=KLJUC, base_url="https://api.deepseek.com")

NAZIV_MODELA = "deepseek-flash"  # ako agent često griješi, probajte "deepseek-v4-pro"


def posalji_modelu(poruke):
    """Pošalje poruke i opise alata modelu, a vrati njegov odgovor."""
    rezultat = klijent.chat.completions.create(
        model=NAZIV_MODELA,
        messages=poruke,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.3,
        max_tokens=400,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return rezultat.choices[0].message
