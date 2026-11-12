import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # učita DEEPSEEK_API_KEY iz datoteke .env

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

odgovor = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "Pozdrav! Jednom rečenicom: tko si?"}],
    max_tokens=100,
    extra_body={"thinking": {"type": "disabled"}},
)

print(odgovor.choices[0].message.content)
print("Potrošeno tokena:", odgovor.usage.total_tokens)