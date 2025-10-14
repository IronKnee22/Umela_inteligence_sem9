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
navstivene = set()

cesta = []


def pohyb(stav):
    navstivene.add(stav)
    cesta.append(stav)

    if bludiste[stav[0]][stav[1]] == "E":
        print("Našel jsem cestu")
        return True

    # dolu
    novy_stav = stav[0] + 1, stav[1]
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and novy_stav not in navstivene
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        if pohyb(novy_stav):
            return True

    # doprava
    novy_stav = stav[0], stav[1] + 1
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and novy_stav not in navstivene
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        if pohyb(novy_stav):
            return True

    # nahoru
    novy_stav = stav[0] - 1, stav[1]
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and novy_stav not in navstivene
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        if pohyb(novy_stav):
            return True

    # doleva
    novy_stav = stav[0], stav[1] - 1
    if (
        0 <= novy_stav[0] < pocet_radku
        and 0 <= novy_stav[1] < pocet_sloupcu
        and novy_stav not in navstivene
        and bludiste[novy_stav[0]][novy_stav[1]] != "#"
    ):
        if pohyb(novy_stav):
            return True

    cesta.pop()
    return False


if pohyb(start_tuple):
    print("Vítězná cesta je:", cesta)
else:
    print("Cesta neexistuje.")
