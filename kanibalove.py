from collections import deque

# 0 => lodka levý břeh, počet osob n levém břehu, Kanibalové, Misionáři
start_tuple = (0, 3, 3)
end_tuple = (1, 0, 0)


def muze_nastat(stav):
    if stav[1] > stav[2] and stav[2] != 0:
        return False
    elif stav[1] < stav[2] and stav[2] != 3:
        return False
    else:
        return True


def presun(stav):
    mozne_stavy = []
    for i in range(3):
        for j in range(3):
            novy_stav = lod(stav, i, j)
            if novy_stav is not None:
                if muze_nastat(novy_stav):
                    mozne_stavy.append(novy_stav)

    return mozne_stavy


def lod(stav, poc_kan, poc_mis):
    if poc_kan + poc_mis > 0 and poc_kan + poc_mis <= 2:
        lod = int(not (stav[0]))
        if lod == 0:
            kan = stav[1] + poc_kan
            mis = stav[2] + poc_mis

        elif lod == 1:
            kan = stav[1] - poc_kan
            mis = stav[2] - poc_mis

        if kan > 3 or mis > 3 or kan < 0 or mis < 0:
            return

        novy_stav = (lod, kan, mis)
        return novy_stav
    else:
        return


def main():
    fronta = deque([(start_tuple, [start_tuple])])
    navstiveny_stav = set()

    while fronta:
        stav, cesta = fronta.popleft()
        navstiveny_stav.add(stav)
        nove_mozne_stavy = presun(stav)

        for novy_stav in nove_mozne_stavy:
            if novy_stav not in navstiveny_stav:
                nova_cesta = cesta + [novy_stav]
                fronta.append((novy_stav, nova_cesta))
                if novy_stav == end_tuple:
                    print("Našel jsem řešení")
                    for i, item in enumerate(nova_cesta):
                        print(f"Krok ciso {i + 1}: {item}")
                    return

    print("Nenašel jsem řešení")


main()
