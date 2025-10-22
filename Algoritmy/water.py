from collections import deque

start_tuple = (0, 0)
end = 4
max_naplneni = (3, 5)


def naplneni(ktera, stav):
    if ktera == 0:
        return (3, stav[1])

    if ktera == 1:
        return (stav[0], 5)


def vyliti(ktera, stav):
    if ktera == 0:
        return (0, stav[1])

    if ktera == 1:
        return (stav[0], 0)


def preliti(z_ktere, stav):
    zbytek = 0
    soucet = stav[0] + stav[1]

    if z_ktere == 0:
        if soucet > max_naplneni[1]:
            zbytek = soucet - max_naplneni[1]
            return (zbytek, max_naplneni[1])
        return (zbytek, soucet)

    if z_ktere == 1:
        if soucet > max_naplneni[0]:
            zbytek = soucet - max_naplneni[0]
            return (max_naplneni[0], zbytek)
        return (soucet, zbytek)


def tah(stav):
    mozne_stavy = []

    novy_stav = naplneni(0, stav)
    mozne_stavy.append(novy_stav)
    novy_stav = naplneni(1, stav)
    mozne_stavy.append(novy_stav)
    novy_stav = vyliti(0, stav)
    mozne_stavy.append(novy_stav)
    novy_stav = vyliti(1, stav)
    mozne_stavy.append(novy_stav)
    novy_stav = preliti(0, stav)
    mozne_stavy.append(novy_stav)
    novy_stav = preliti(1, stav)
    mozne_stavy.append(novy_stav)

    return mozne_stavy


def main():
    fronta = deque([(start_tuple, [start_tuple])])
    navstivene_stavy = set()

    while fronta:
        soucasny_stav, cesta = fronta.popleft()
        navstivene_stavy.add(soucasny_stav)
        mozne_stavy = tah(soucasny_stav)
        for item in mozne_stavy:
            if item not in navstivene_stavy:
                nova_cesta = cesta + [item]
                fronta.append((item, nova_cesta))

                if item[0] == end or item[1] == end:
                    print("Našel jsem řešení")
                    for i, krok in enumerate(nova_cesta):
                        print(f"{i}. {krok}")
                    return


main()
