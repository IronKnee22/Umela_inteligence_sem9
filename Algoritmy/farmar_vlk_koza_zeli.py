from collections import deque

start_tuple = (0, 0, 0, 0)
end_tuple = (1, 1, 1, 1)


def bezpecny_stav(stav):
    if stav[1] == stav[2] and stav[0] != stav[2]:
        return False
    elif stav[2] == stav[3] and stav[0] != stav[2]:
        return False
    else:
        return True


def presun(stav, kdo_presun):
    f = int(not (stav[0]))
    v = stav[1]
    k = stav[2]
    z = stav[3]

    if kdo_presun == 1:
        v = int(not (stav[1]))
    elif kdo_presun == 2:
        k = int(not (stav[2]))
    elif kdo_presun == 3:
        z = int(not (stav[3]))

    novy_stav = (f, v, k, z)

    return novy_stav


def muzu_presun(stav, kdo_presun):
    if stav[0] == stav[kdo_presun]:
        return True
    else:
        return False


def generuj_mozne_stavy(stav):
    mozne_stavy = []

    for i in range(4):
        if muzu_presun(stav, i):
            novy_stav = presun(stav, i)
            if bezpecny_stav(novy_stav):
                mozne_stavy.append(novy_stav)

    return mozne_stavy


def main():
    fronta = deque([(start_tuple, [start_tuple])])
    navstivene_stavy = set()

    while fronta:
        soucasny_stav, cesta = fronta.popleft()
        navstivene_stavy.add(soucasny_stav)
        mozne_stavy = generuj_mozne_stavy(soucasny_stav)
        for item in mozne_stavy:
            if item not in navstivene_stavy:
                pokracovani_cesta = cesta + [item]
                fronta.append((item, pokracovani_cesta))
                if item == end_tuple:
                    print("Našel jsem správný postup")
                    for item2 in pokracovani_cesta:
                        print(item2)
                    return


main()
