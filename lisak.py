import heapq

start_stav = ((8, 6, 7), (2, 5, 4), (3, 0, 1))


cil_stav = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

pocet_radku = len(start_stav)
pocet_sloupcu = len(start_stav[0])

cilove_pozice = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    0: (2, 2),
}

open_list = []
g_skore = {start_stav: 0}
rodice = {start_stav: None}
closed_list = set()


def vytiskni_desku(stav):
    print("-------")
    for radek in stav:
        print(f"| {' '.join(str(c) if c != 0 else '.' for c in radek)} |")
    print("-------")


def rekonstruuj_cestu(rodice, start, cil):
    cesta = []
    aktualni = cil
    while aktualni is not None:
        cesta.append(aktualni)
        aktualni = rodice.get(aktualni)

    return cesta[::-1]


def main():
    h_skore = odhad_heuristiky(start_stav)
    f_skore = g_skore[start_stav] + h_skore

    heapq.heappush(open_list, (f_skore, start_stav))

    while open_list:
        aktualni_f, aktualni_pozice = heapq.heappop(open_list)
        if aktualni_pozice in closed_list:
            continue
        closed_list.add(aktualni_pozice)

        if aktualni_pozice == cil_stav:
            print("Našel jsem nejkratší cestu:")
            finalni_cesta = rekonstruuj_cestu(rodice, start_stav, cil_stav)
            for i, krok in enumerate(finalni_cesta):
                print(f"\nKrok {i}:")
                vytiskni_desku(krok)  # Použijeme novou funkci
            return

        mozne_stavy = pohyb(aktualni_pozice)

        for soused in mozne_stavy:
            if soused not in closed_list:
                tentativni_g_skore = g_skore[aktualni_pozice] + 1
                if tentativni_g_skore < g_skore.get(soused, float("inf")):
                    rodice[soused] = aktualni_pozice
                    g_skore[soused] = tentativni_g_skore
                    h_skore = odhad_heuristiky(soused)
                    f_skore = g_skore[soused] + h_skore
                    heapq.heappush(open_list, (f_skore, soused))
    print("Nemá řešení")


def pohyb(stav):
    mozne_stavy = []
    pohyby = ((-1, 0), (0, 1), (1, 0), (0, -1))

    for i in range(pocet_radku):
        for j in range(pocet_sloupcu):
            if stav[i][j] == 0:
                for smer in pohyby:
                    if (
                        0 <= i + smer[0] < pocet_radku
                        and 0 <= j + smer[1] < pocet_sloupcu
                    ):
                        temp_list = list(stav)
                        temp_list[i] = list(temp_list[i])
                        temp_list[i + smer[0]] = list(temp_list[i + smer[0]])

                        temp_list[i][j], temp_list[i + smer[0]][j + smer[1]] = (
                            temp_list[i + smer[0]][j + smer[1]],
                            temp_list[i][j],
                        )

                        temp_list[i] = tuple(temp_list[i])
                        temp_list[i + smer[0]] = tuple(temp_list[i + smer[0]])
                        new_tuple = tuple(temp_list)
                        mozne_stavy.append(new_tuple)
    return mozne_stavy


def odhad_heuristiky(stav):
    h = 0
    for i in range(3):
        for j in range(3):
            zkoumany_objekt = stav[i][j]

            cil_radek, cil_sloupec = cilove_pozice[zkoumany_objekt]

            h += abs(i - cil_radek) + abs(j - cil_sloupec)

    return h


main()
