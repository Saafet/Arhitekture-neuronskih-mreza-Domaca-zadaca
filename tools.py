import json
from datetime import datetime


# ---------- 1. Alati: obične Python funkcije ----------
def trenutno_vrijeme():
    return datetime.now().strftime("%d.%m.%Y. %H:%M")


def izracunaj(a, b, operacija):
    if operacija == "+":
        return a + b
    if operacija == "-":
        return a - b
    if operacija == "*":
        return a * b
    if operacija == "/":
        return a / b if b != 0 else "Greška: dijeljenje s nulom"
    return "Nepoznata operacija"


def spremi_biljesku(tekst):
    with open("biljeske.txt", "a", encoding="utf-8") as f:
        f.write(tekst + "\n")
    return "Bilješka je spremljena."


FUNKCIJE = {
    "trenutno_vrijeme": trenutno_vrijeme,
    "izracunaj": izracunaj,
    "spremi_biljesku": spremi_biljesku,
}


# ---------- 2. Opisi alata za model ----------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "trenutno_vrijeme",
            "description": "Vraća današnji datum i trenutno vrijeme.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "izracunaj",
            "description": "Računa a operacija b. Koristi za svaki račun.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                    "operacija": {"type": "string", "enum": ["+", "-", "*", "/"]},
                },
                "required": ["a", "b", "operacija"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "spremi_biljesku",
            "description": "Sprema kratku bilješku korisnika u datoteku.",
            "parameters": {
                "type": "object",
                "properties": {"tekst": {"type": "string", "description": "Tekst bilješke"}},
                "required": ["tekst"],
            },
        },
    },
]


# ---------- 3. Izvršavanje alata koji je model zatražio ----------
def izvrsi_alat(ime, argumenti_json):
    try:
        argumenti = json.loads(argumenti_json)
        return FUNKCIJE[ime](**argumenti)
    except Exception as e:  # greška ide modelu, program se ne ruši
        return f"Greška: {e}"