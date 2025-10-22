from collections import deque

start_tuple = (" ", "B", "B", " ", "W", "W", " ")
end_tuple = (" ", "W", "W", " ", "B", "B", " ")


def pohyb(stav):
    mozne_stavy = []

    for i in range(7):
        if stav[i] != " ":
            nove_stav_posun = posun(stav, i)
            if nove_stav_posun is not None:
                for novy_stav_posun in nove_stav_posun:
                    if novy_stav_posun is not None:
                        mozne_stavy.append(novy_stav_posun)

            nove_stav_skok = skok(stav, i)
            if nove_stav_skok is not None:
                for novy_stav_skok in nove_stav_skok:
                    if novy_stav_skok is not None:
                        mozne_stavy.append(novy_stav_skok)

    return mozne_stavy


def posun(stav, pozice):
    mozne_stavy = []
    temp_stav = list(stav)
    for i in [-1, 1]:
        if (
            (pozice + 2 * i) < len(stav)
            and (pozice + 2 * i) > 0
            and stav[pozice + i] == " "
        ):
            temp_stav[pozice + i] = stav[pozice]
            temp_stav[pozice] = stav[pozice + i]
            novy_stav = (
                temp_stav[0],
                temp_stav[1],
                temp_stav[2],
                temp_stav[3],
                temp_stav[4],
                temp_stav[5],
                temp_stav[6],
            )
            mozne_stavy.append(novy_stav)
    return mozne_stavy


def skok(stav, pozice):
    mozne_stavy = []
    temp_stav = list(stav)
    for i in [-1, 1]:
        if (
            (pozice + 2 * i) < len(stav)
            and (pozice + 2 * i) > 0
            and stav[pozice + i] != " "
            and stav[pozice + 2 * i] == " "
        ):
            temp_stav[pozice + 2 * i] = stav[pozice]
            temp_stav[pozice] = stav[pozice + 2 * i]
            novy_stav = (
                temp_stav[0],
                temp_stav[1],
                temp_stav[2],
                temp_stav[3],
                temp_stav[4],
                temp_stav[5],
                temp_stav[6],
            )
            mozne_stavy.append(novy_stav)
    return mozne_stavy


def main():
    fronta = deque([(start_tuple, [start_tuple])])
    navstiveno = set()

    while fronta:
        stav, cesta = fronta.popleft()
        navstiveno.add(stav)
        mozne_stavy = pohyb(stav)

        for item in mozne_stavy:
            if item not in navstiveno:
                nova_cesta = cesta + [item]
                fronta.append((item, nova_cesta))

                if item == end_tuple:
                    print("Našel jsem řešení")
                    for i, item2 in enumerate(nova_cesta):
                        tuple_string = "".join(item2)
                        upraveny_string = (
                            tuple_string.replace("W", "⚪")
                            .replace("B", "⚫")
                            .replace(" ", "🟩")
                        )
                        print(f"Pokus číslo {i}: {upraveny_string}")
                    return

    print("Nic jsem nenašel")


main()
