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
end = "E"

open_list = []
g_skore = {start_tuple: 0}
rodice = {start_tuple: None}
closed_list = set()


def odhad_heuristika(stav, cil):
    # Manhatonovska
    vysledek = abs(stav[0] - cil[0]) + abs(stav[1] - cil[1])
    return vysledek


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


def rekonstruuj_cestu(rodice, start, cil):
    cesta = []
    aktualni = cil
    while aktualni is not None:
        cesta.append(aktualni)
        aktualni = rodice.get(aktualni)

    return cesta[::-1]


def main():
    h_skore = odhad_heuristika(start_tuple, end_tuple)
    f_skore = g_skore[start_tuple] + h_skore

    heapq.heappush(open_list, (f_skore, start_tuple))

    while open_list:
        aktualni_f, aktualni_pozice = heapq.heappop(open_list)
        if aktualni_pozice in closed_list:
            continue
        closed_list.add(aktualni_pozice)

        if aktualni_pozice == end_tuple:
            print("Našel jsem nejkratší cestu:")

            finalni_cesta = rekonstruuj_cestu(rodice, start_tuple, end_tuple)

            for i, krok in enumerate(finalni_cesta):
                print(f"{i}. {krok}")
            return

        mozne_stavy = pohyb(aktualni_pozice)

        for soused in mozne_stavy:
            if soused not in closed_list:
                tentativni_g_skore = g_skore[aktualni_pozice] + 1
                if tentativni_g_skore < g_skore.get(soused, float("inf")):
                    rodice[soused] = aktualni_pozice
                    g_skore[soused] = tentativni_g_skore
                    h_skore = odhad_heuristika(soused, end_tuple)
                    f_skore = g_skore[soused] + h_skore
                    heapq.heappush(open_list, (f_skore, soused))


main()
