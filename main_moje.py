from llm_moje import posalji_modelu
from tools_moje import izvrsi_alat

UPUTA = (
    "Ti si asistent za dnevnik filmova. Odgovaraj kratko i na hrvatskom. "
    "Za spremanje filmova, popis i prosjek ocjena obavezno koristi alate."
)
MAKS_PORUKA = 20


def ogranici_povijest(poruke, maks=MAKS_PORUKA):
    """Ostavi uputu i zadnjih ~maks poruka, počevši od korisnikove poruke."""
    if len(poruke) <= maks + 1:
        return poruke
    start = len(poruke) - maks
    while poruke[start]["role"] != "user":
        start += 1
    return [poruke[0]] + poruke[start:]


def obradi_pitanje(poruke):
    """Vrti petlju dok model traži alate, a na kraju ispiše konačni odgovor."""
    while True:
        odgovor = posalji_modelu(poruke)
        poruke.append(odgovor.model_dump(exclude_none=True))

        if not odgovor.tool_calls:
            print("Agent:", odgovor.content)
            return

        for poziv in odgovor.tool_calls:  # model može tražiti više alata odjednom
            ime = poziv.function.name
            argumenti = poziv.function.arguments
            rezultat = izvrsi_alat(ime, argumenti)
            print(f"  [alat] {ime}({argumenti}) -> {rezultat}")
            poruke.append({"role": "tool", "tool_call_id": poziv.id, "content": str(rezultat)})


def main():
    poruke = [{"role": "system", "content": UPUTA}]
    print("Dnevnik filmova je spreman. Upiši 'izlaz' za kraj.")

    while True:
        unos = input("\nTi: ").strip()
        if unos.lower() == "izlaz":
            break
        if not unos:
            continue
        poruke.append({"role": "user", "content": unos})
        obradi_pitanje(poruke)
        poruke = ogranici_povijest(poruke)


if __name__ == "__main__":
    main()
