from collections import deque

bludiste = [
    ["S", ".", ".", "#", ".", "."],
    [".", "#", ".", "#", ".", "#"],
    [".", "#", ".", ".", ".", "."],
    [".", ".", "#", "#", ".", "."],
    ["#", ".", ".", ".", "#", "E"],
]

start_tuple = (0, 0)
end = "E"

pocet_radku = len(bludiste)
pocet_sloupcu = len(bludiste[0])


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


def main():
    zasobnik = deque([(start_tuple, [start_tuple])])
    navstivene_stavy = set()

    while zasobnik:
        soucasny_stav, cesta = zasobnik.pop()
        navstivene_stavy.add(soucasny_stav)
        mozne_stavy = pohyb(soucasny_stav)
        for item in mozne_stavy:
            if item not in navstivene_stavy:
                nova_cesta = cesta + [item]
                zasobnik.append((item, nova_cesta))

                if bludiste[item[0]][item[1]] == "E":
                    print("Našel jsem cestu")
                    for i, krok in enumerate(nova_cesta):
                        print(f"{i}. {krok}")
                    return


main()
