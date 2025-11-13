import math
import random

import matplotlib.pyplot as plt

random.seed(10 * 1)
velikost_populace = 1000
pocet_generaci = 50

list_mesta = []


def vytvor_mesta():
    global list_mesta
    list_poradi = []
    for i in range(15):
        mesto = (random.randint(0, 100), random.randint(0, 100))
        list_mesta.append(mesto)
        list_poradi.append(i)
    return list_poradi


def euklid_vzdalenost(souradnice1, souradnice2):
    vzdalenost = math.sqrt(
        (souradnice2[0] - souradnice1[0]) ** 2 + (souradnice2[1] - souradnice1[1]) ** 2
    )
    return vzdalenost


def fit_jedinec(jedinec):
    hodnota = 0
    temp_predchozi = None
    for i, pozice in enumerate(jedinec):
        temp_soucasne = pozice
        if i == len(jedinec) - 1:
            hodnota += euklid_vzdalenost(
                list_mesta[temp_predchozi], list_mesta[temp_soucasne]
            )
            temp_predchozi = temp_soucasne
            hodnota += euklid_vzdalenost(
                list_mesta[temp_predchozi], list_mesta[jedinec[0]]
            )
        elif i > 0:
            hodnota += euklid_vzdalenost(
                list_mesta[temp_predchozi], list_mesta[temp_soucasne]
            )
        temp_predchozi = temp_soucasne
    return hodnota


def vytvor_generaci(list_poradi):
    populace = []
    for i in range(velikost_populace):
        temp = list_poradi.copy()
        random.shuffle(temp)
        fitness = fit_jedinec(temp)
        temp_dict = {"cesta": temp, "fitness": fitness}
        populace.append(temp_dict)
    return populace


def mutace(populace):
    nova_populace = populace.copy()
    for i, jedinec in enumerate(populace):
        rodic = jedinec["cesta"]
        if i == 0:
            potomek_cesta = rodic.copy()
            fitness = jedinec["fitness"]
        else:
            potomek_cesta = rodic.copy()
            mutation_chance = 0
            while True:
                if random.randint(0, mutation_chance) <= 0:
                    mutation_chance += 1
                    pozice1 = random.randrange(len(rodic))
                    pozice2 = random.randrange(len(rodic))
                    potomek_cesta[pozice1], potomek_cesta[pozice2] = (
                        potomek_cesta[pozice2],
                        potomek_cesta[pozice1],
                    )
                else:
                    break
            fitness = fit_jedinec(potomek_cesta)
        potomek = {"cesta": potomek_cesta, "fitness": fitness}
        nova_populace.append(potomek)
    return nova_populace


def nakresli_graf_vyvoje(historie):
    plt.figure(figsize=(10, 6))
    plt.plot(historie)
    plt.title("Vývoj fitness (délky cesty) napříč generacemi")
    plt.xlabel("Generace")
    plt.ylabel("Délka nejlepší cesty (Fitness)")
    plt.grid(True)
    plt.savefig("vyvoj_fitness.png")
    print("Graf vývoje fitness uložen jako 'vyvoj_fitness.png'")


def nakresli_graf_cesty(nejlepsi_jedinec, mesta):
    cesta = nejlepsi_jedinec["cesta"]
    souradnice_x = []
    souradnice_y = []

    for index_mesta in cesta:
        souradnice_x.append(mesta[index_mesta][0])
        souradnice_y.append(mesta[index_mesta][1])

    souradnice_x.append(mesta[cesta[0]][0])
    souradnice_y.append(mesta[cesta[0]][1])

    plt.figure(figsize=(10, 8))
    plt.plot(souradnice_x, souradnice_y, "o-")

    for i, index_mesta in enumerate(cesta):
        plt.text(mesta[index_mesta][0] + 0.5, mesta[index_mesta][1] + 0.5, str(i))

    plt.title(f"Nejlepší nalezená cesta (Délka: {nejlepsi_jedinec['fitness']:.2f})")
    plt.xlabel("X souřadnice")
    plt.ylabel("Y souřadnice")
    plt.grid(True)
    plt.savefig("nejlepsi_cesta.png")
    print("Graf nejlepší cesty uložen jako 'nejlepsi_cesta.png'")


def main():
    list_poradi = vytvor_mesta()
    populace = vytvor_generaci(list_poradi)
    historie_fitness = []

    print(f"Start... běží {pocet_generaci} generací s populací {velikost_populace}.")

    for i in range(pocet_generaci):
        populace = sorted(populace, key=lambda item: item["fitness"])

        nejlepsi_z_generace = populace[0]
        historie_fitness.append(nejlepsi_z_generace["fitness"])

        if i % 100 == 0:
            print(
                f"Generace {i}: Nejlepší fitness = {nejlepsi_z_generace['fitness']:.2f}"
            )

        nova_populace = mutace(populace)
        nova_populace_sort = sorted(nova_populace, key=lambda item: item["fitness"])
        populace = nova_populace_sort[:velikost_populace]

    print("\n--- Evoluce dokončena ---")

    nejlepsi_cesta_celkove = populace[0]

    print("Nejlepší nalezená cesta:")
    print(nejlepsi_cesta_celkove)

    nakresli_graf_vyvoje(historie_fitness)
    nakresli_graf_cesty(nejlepsi_cesta_celkove, list_mesta)


main()
