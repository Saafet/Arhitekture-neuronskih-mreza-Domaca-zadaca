# AI agent: dnevnik filmova

**Tema:** dnevnik pogledanih filmova. Agent u terminalu razgovara s modelom `deepseek-flash` (DeepSeek API) i po potrebi poziva tri vlastita alata. Filmovi se spremaju u datoteku `filmovi.txt`.

## Pokretanje

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# u datoteku .env upišite: DEEPSEEK_API_KEY=sk-...
python main_moje.py
```

## Datoteke

- `main_moje.py` – razgovor u terminalu i petlja agenta
- `llm_moje.py` – spajanje na DeepSeek i funkcija `posalji_modelu`
- `tools_moje.py` – tri alata, njihovi opisi i `izvrsi_alat`

## Alati (`tools_moje.py`)

| Alat | Argumenti | Opis |
|------|-----------|------|
| `dodaj_film` | `naslov`, `ocjena` | Sprema film s ocjenom od 1 do 10 u `filmovi.txt`. |
| `popis_filmova` | `min_ocjena` (neobavezno) | Vraća popis filmova, po želji samo one s ocjenom jednakom ili višom od zadane. |
| `prosjecna_ocjena` | nema | Vraća prosjek ocjena svih spremljenih filmova. |

## Ispis iz terminala

(.venv) C:\Users\Administrator\Desktop\moj-agent>python main_moje.py
Dnevnik filmova je spreman. Upiši 'izlaz' za kraj.

Ti: Dodaj film Inception s ocjenom 9
  [alat] dodaj_film({"naslov": "Inception", "ocjena": 9}) -> Spremljeno: Inception (9/10).
Agent: Dodano: Inception (9/10).

Ti: Dodaj Shrek 2 s ocjenom 7.5 i reci mi koliki je prosjek
  [alat] dodaj_film({"naslov": "Shrek 2", "ocjena": 7.5}) -> Spremljeno: Shrek 2 (7.5/10).
  [alat] prosjecna_ocjena({}) -> Prosječna ocjena je 8.25 na temelju 2 filmova.
Agent: Dodano: Shrek 2 (7.5/10). Prosjek je 8.25 (2 filma).

Ti: Koji su filmovi s ocjenom 8 ili više?
  [alat] popis_filmova({"min_ocjena": 8}) -> - Inception: 9/10
Agent: Filmovi s ocjenom 8 ili više:
- Inception: 9/10

Ti: izlaz
