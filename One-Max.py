import random

dokonala_bytost = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

populatoin = 100

mutation_chance = 0.01


def mutace(potomek):
    mutace = potomek

    if random.random() < mutation_chance:
        index_k_mutaci = random.randint(0, len(mutace["chromozom"]) - 1)
        mutace["chromozom"][index_k_mutaci] = int(
            not (mutace["chromozom"][index_k_mutaci])
        )
        mutace["fitness"] = spocitej_fitness(mutace["chromozom"])

    return mutace


def vytvoreni_populace():
    individuals = []
    for i in range(populatoin):
        temp = []
        for j, _ in enumerate(dokonala_bytost):
            k = random.randint(0, 1)
            temp.append(k)

        fitness = spocitej_fitness(temp)
        temp_dict = {"chromozom": temp, "fitness": fitness}
        individuals.append(temp_dict)

    return individuals


def spocitej_fitness(jedinec):
    count = 0
    for item in jedinec:
        count += item

    return count


def turnaj(populace):
    rodice = []
    for j in range(2):
        soutezici = []
        for i in range(3):
            soutezici.append(random.choice(populace))

        rodice.append(max(soutezici, key=lambda jedinec: jedinec["fitness"]))

    return rodice


def proved_krizeni(rodice):
    rodic1 = rodice[0]
    rodic2 = rodice[1]

    chrom_1 = rodic1["chromozom"]
    chrom_2 = rodic2["chromozom"]

    bod_zlomu = random.randint(1, len(chrom_1) - 1)

    potomek_chrom = chrom_1[:bod_zlomu] + chrom_2[bod_zlomu:]
    fitness = spocitej_fitness(potomek_chrom)
    potomek = {"chromozom": potomek_chrom, "fitness": fitness}

    return potomek


def main():
    populace = vytvoreni_populace()
    i = 0

    while True:
        i += 1

        rodice = turnaj(populace)
        populace.append(mutace(proved_krizeni(rodice)))

        if populace[-1]["chromozom"] == dokonala_bytost:
            print("Našel jsem dokonalou bytost")
            print(f"Trvalo to {i} křížení")

            return


main()
