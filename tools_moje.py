import json

DATOTEKA = "filmovi.txt"
RAZDVOJNIK = ";"


# ---------- pomoćna funkcija ----------
def _procitaj_filmove():
    """Vrati listu (naslov, ocjena) iz datoteke; prazna lista ako datoteka ne postoji."""
    filmovi = []
    try:
        with open(DATOTEKA, "r", encoding="utf-8") as datoteka:
            for linija in datoteka:
                linija = linija.strip()
                if linija:
                    naslov, ocjena = linija.rsplit(RAZDVOJNIK, 1)
                    filmovi.append((naslov, float(ocjena)))
    except FileNotFoundError:
        pass
    return filmovi


# ---------- 1. Alati: obične Python funkcije ----------
def dodaj_film(naslov, ocjena):
    if not 1 <= ocjena <= 10:
        return "Greška: ocjena mora biti između 1 i 10."
    with open(DATOTEKA, "a", encoding="utf-8") as datoteka:
        datoteka.write(f"{naslov}{RAZDVOJNIK}{ocjena}\n")
    return f"Spremljeno: {naslov} ({ocjena}/10)."


def popis_filmova(min_ocjena=0):
    odabrani = [f for f in _procitaj_filmove() if f[1] >= min_ocjena]
    if not odabrani:
        return "Nema filmova za prikaz."
    return "\n".join(f"- {naslov}: {ocjena:g}/10" for naslov, ocjena in odabrani)


def prosjecna_ocjena():
    filmovi = _procitaj_filmove()
    if not filmovi:
        return "Dnevnik je prazan."
    zbroj = sum(ocjena for _, ocjena in filmovi)
    return f"Prosječna ocjena je {zbroj / len(filmovi):.2f} na temelju {len(filmovi)} filmova."


FUNKCIJE = {
    "dodaj_film": dodaj_film,
    "popis_filmova": popis_filmova,
    "prosjecna_ocjena": prosjecna_ocjena,
}


# ---------- 2. Opisi alata za model ----------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "dodaj_film",
            "description": "Upisuje pogledani film u dnevnik zajedno s ocjenom od 1 do 10.",
            "parameters": {
                "type": "object",
                "properties": {
                    "naslov": {"type": "string", "description": "Naslov filma"},
                    "ocjena": {"type": "number", "description": "Ocjena od 1 do 10"},
                },
                "required": ["naslov", "ocjena"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "popis_filmova",
            "description": "Ispisuje filmove iz dnevnika s ocjenama. Parametar min_ocjena filtrira filmove s ocjenom jednakom ili višom od zadane.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_ocjena": {"type": "number", "description": "Neobavezno: najmanja ocjena filma"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "prosjecna_ocjena",
            "description": "Računa prosječnu ocjenu svih filmova u dnevniku. Koristi kad korisnik pita za prosjek.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


# ---------- 3. Izvršavanje alata koji je model zatražio ----------
def izvrsi_alat(ime, argumenti_json):
    if ime not in FUNKCIJE:
        return f"Greška: nepoznat alat '{ime}'."
    try:
        argumenti = json.loads(argumenti_json or "{}")
        return FUNKCIJE[ime](**argumenti)
    except Exception as greska:  # greška ide modelu, program se ne ruši
        return f"Greška: {greska}"
