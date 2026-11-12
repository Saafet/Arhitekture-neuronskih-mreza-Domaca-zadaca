from llm import pitaj_model
from tools import izvrsi_alat

SYSTEM_PORUKA = "Ti si kratak osobni asistent. Odgovaraj na hrvatskom. Za račun, vrijeme i bilješke koristi alate."


def skrati_povijest(messages, najvise=20):
    """Zadrži system poruku i zadnjih ~20 poruka, počevši od korisnikove."""
    if len(messages) <= najvise + 1:
        return messages
    pocetak = len(messages) - najvise
    while messages[pocetak]["role"] != "user":
        pocetak += 1
    return [messages[0]] + messages[pocetak:]


def main():
    messages = [{"role": "system", "content": SYSTEM_PORUKA}]
    print("Agent je spreman. Upiši 'izlaz' za kraj.")

    while True:
        pitanje = input("\nTi: ")
        if pitanje.lower() == "izlaz":
            break
        messages.append({"role": "user", "content": pitanje})

        while True:  # vrti dok model traži alate
            odgovor = pitaj_model(messages)
            messages.append(odgovor.model_dump(exclude_none=True))

            if not odgovor.tool_calls:  # nema alata → konačni odgovor
                print("Agent:", odgovor.content)
                break

            for poziv in odgovor.tool_calls:  # model može tražiti više alata odjednom
                rezultat = izvrsi_alat(poziv.function.name, poziv.function.arguments)
                print(f"  [alat] {poziv.function.name}({poziv.function.arguments}) -> {rezultat}")
                messages.append({"role": "tool", "tool_call_id": poziv.id, "content": str(rezultat)})

        messages = skrati_povijest(messages)


if __name__ == "__main__":
    main()