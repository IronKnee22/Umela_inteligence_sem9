import heapq

bludiste = [
    ["S", ".", ".", "#", ".", "."],
    [".", "#", ".", "#", ".", "#"],
    [".", "#", ".", ".", ".", "."],
    [".", ".", "#", "#", ".", "."],
    ["#", ".", ".", ".", "#", "E"],
]

pocet_radku = len(bludiste)
pocet_sloupcu = len(bludiste[0])

start_tuple = (0, 0)
end_tuple = (4, 5)

# f = g * h

g = {start_tuple: 0}
rodice = {start_tuple: None}

open_seznam = []
closed_seznam = set()


def rekonstruuj_cestu(rodice, start, cil):
    cesta = []
    aktualni = cil
    while aktualni is not None:
        cesta.append(aktualni)
        aktualni = rodice.get(aktualni)
    return cesta[::-1]


def main():
    h = odhad_heuristiky(start_tuple, end_tuple)
    f = g[start_tuple] + h
    heapq.heappush(open_seznam, (f, start_tuple))

    while open_seznam:
        f, soucasny_stav = heapq.heappop(open_seznam)
        closed_seznam.add(soucasny_stav)
        mozne_stavy = pohyb(soucasny_stav)

        if soucasny_stav == end_tuple:
            print("Našel jsem nejkratší cestu:")
            finalni_cesta = rekonstruuj_cestu(rodice, start_tuple, end_tuple)
            for i, krok in enumerate(finalni_cesta):
                print(f"{i}. {krok}")
            break  # nebo return

        for potomek in mozne_stavy:
            if potomek not in closed_seznam:
                soucasne_g = g[soucasny_stav] + 1
                if soucasne_g < g.get(potomek, float("inf")):
                    rodice[potomek] = soucasny_stav
                    g[potomek] = soucasne_g

                    h = odhad_heuristiky(potomek, end_tuple)
                    f = g[potomek] + h
                    heapq.heappush(open_seznam, (f, potomek))


def odhad_heuristiky(stav, cil):
    return abs(stav[0] - cil[0]) + abs(stav[1] - cil[1])


def pohyb(stav):
    mozne_stavy = []
    # dolu
    novy_stav = stav[0] + 1, stav[1]
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        mozne_stavy.append(novy_stav)
    # doprava
    novy_stav = stav[0], stav[1] + 1
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        mozne_stavy.append(novy_stav)
    # nahoru
    novy_stav = stav[0] - 1, stav[1]
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        mozne_stavy.append(novy_stav)
    # doleva
    novy_stav = stav[0], stav[1] - 1
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        mozne_stavy.append(novy_stav)

    return mozne_stavy


main()
