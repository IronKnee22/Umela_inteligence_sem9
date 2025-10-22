import random
import sys

import matplotlib.pyplot as plt
import numpy as np

from grayxbinary import *

# konstanta delky chromosonu
DELKARETEZCU = 20

# konstanta velikosti populace v jedne generaci
NUMGEN = 10

# pravdepodobnost krizeni
KRIZENIPROB = 0.9

# pravdepodobnost mutace
MUTACEPROB = 0.5

# dolni mez pro definicni obor funkce
DMEZ = -5

# horni mez pro definicni obor funkce
HMEZ = 5

LOGFITNESS = False
LOG = True


def fce(poloha):
    # vraci hodnotu fitness funkce pro jedince
    # poloha je decimalni cislo prevedene z chromosonu jedince
    x = DMEZ + poloha * (HMEZ - DMEZ) / (pow(2, DELKARETEZCU) - 1)
    # y = 40*(x-(x*x))+1300
    y = (x + 1.5) * (x - 0.5) * np.sin(4 * x - 1) + 50
    if LOGFITNESS:
        print(x)
        print(y)
    return y


###
# Prevadi retezec z grayova kodu na desitkove cislo
###
def dekod(retezec):
    binarni = graytobinary(retezec)
    # binarni = retezec
    result = 0
    k = 1
    # prevod binarniho cisla na desitkove
    for index in range(1, len(binarni) + 1):
        s = binarni[-index]
        cislo = int(s)
        result += k * cislo
        k = k * 2
    return result


###
# Najde pole rulety, do kterého padla hodnota
# TODO vyhledavat pomoci puleni intervalu
###
def vyhledej(hodnota, ruleta):
    # predelat na puleni intervalu
    for index in range(len(ruleta)):
        if hodnota < ruleta[index]:
            return index
    return len(ruleta) - 1


def reprodukce(oldgenerace):
    ruleta = []
    novagenerace = []
    minimum = sys.float_info.max
    maximum = sys.float_info.min
    nej = ""
    soucet = 0

    # vynuluje ruletu
    for _ in range(0, len(oldgenerace)):
        ruleta.append(0.0)

    # prvni kolo vytvareni rulety - vypocet fitness funkce a souctu fitness pres celou generaci
    for i in range(0, len(oldgenerace)):
        # print(oldgenerace[i])
        akthodnota = fce(dekod(oldgenerace[i]))
        # print(akthodnota)
        if akthodnota < minimum:
            minimum = akthodnota
        if akthodnota > maximum:
            maximum = akthodnota
            nej = oldgenerace[i]
        ruleta[i] = akthodnota
        soucet = soucet + akthodnota

    if LOG:
        print("soucet: " + str(soucet))
        print("maximum: " + str(maximum))
        print("jedinec: " + str(nej))
        print("************************************************************")

    if minimum < 0:
        print("Funkce obsahuje na zkoumaném intervalu hodnoty menší než 0")
        exit(1)

    if soucet == 0:
        soucet = 1

    # druhe kolo vytvareni rulety - prirazeni prostoru na ruletovem kole pro jednotlive jedince
    # vypoctena fitness jedince je nejaka cast z celeho souctu a tuto cast zaujimaji na rulete a je to jejich
    # pravdepodobnost, ze budou behem selekce vzbrani do dalsi generace
    # soucet = 100%
    ruleta[0] = ruleta[0] / soucet
    for i in range(1, NUMGEN - 1):
        ruleta[i] = ruleta[i - 1] + ruleta[i] / soucet
    ruleta[NUMGEN - 1] = 1

    for i in range(NUMGEN):
        # zatočíme na ruletě a reprodukujeme
        hodnota = random.random()
        novagenerace.append(generace[vyhledej(hodnota, ruleta)])

    # krizeni
    novagenkrizeni = []
    while len(novagenerace) > 2:
        # krizeni rodic1; zaroven ho vyrazujeme z populace, aby se znovu nekrizil
        pozicerodic1 = random.randint(0, len(novagenerace) - 1)
        rodic1 = novagenerace[pozicerodic1]
        novagenerace.pop(pozicerodic1)

        # krizeni rodic2; zaroven ho vyrazujeme z populace, aby se znovu nekrizil
        pozicerodic2 = random.randint(0, len(novagenerace) - 1)
        rodic2 = novagenerace[pozicerodic2]
        novagenerace.pop(pozicerodic2)

        # pravdepodobnost krizeni je KRIZENIPROB
        mince = random.random()
        if mince < KRIZENIPROB:
            # krizime v jednobodove v bode pozice
            pozice = random.randint(0, DELKARETEZCU - 1)
            potomek1 = rodic1[0:pozice] + rodic2[pozice:]
            potomek2 = rodic2[0:pozice] + rodic1[pozice:]
            novagenkrizeni.append(potomek1)
            novagenkrizeni.append(potomek2)
        else:
            # do dalsi generace davame rodice, ktere jsme nekrizili
            novagenkrizeni.append(rodic1)
            novagenkrizeni.append(rodic2)

    # do dalsi generace dame nejlepsiho jedince, abychom o nej neprisli pri krizeni a mutaci
    for k in novagenerace:
        novagenkrizeni.append(nej)

    # mutace mimo poslednich dvou - to jsou nejlepsi jedinci, zalezi na poctu jedincu v generaci
    # pokud je to cislo liche, kopirujeme jednoho, pokud sude dva
    for i in range(NUMGEN - 2):
        # pravdepodobnost mutace je MUTACEPROB
        mince = random.random()
        if mince < MUTACEPROB:
            # vybranou pozici otocime bud 1->0 nebo 0->1
            # programatorska poznamka - v Pythonu je string immutable a musi se vytvorit novy string
            pozice = random.randint(0, DELKARETEZCU - 2)
            clen = (
                novagenkrizeni[i][0:pozice]
                + flip(novagenkrizeni[i][pozice])
                + novagenkrizeni[i][pozice + 1 :]
            )
            novagenkrizeni[i] = clen

    return novagenkrizeni


###############################################################################################
#  Hlavni program
###############################################################################################

# vykresleni fitness funkce
x = np.arange(-5, 5, 0.01)
y = (x + 1.5) * (x - 0.5) * np.sin(4 * x - 1) + 50
# y2 = 40*(x-(x*x))+1300
plt.plot(x, y)
plt.show()

generace = []

for _ in range(NUMGEN):
    dec = random.randint(0, pow(2, DELKARETEZCU) - 1)
    binary = dectobinary(dec, DELKARETEZCU)
    generace.append(binarytogray(binary))

# max aktualni maximum, poradi je cislo generace, zmena je cislo generace kdy se zmenilo maximum
max = 0
poradi = 0
zmena = 0
# pokud po 5 generaci nedojde ke zmene maxima, ukonci prohledavani
while poradi - zmena < 5:
    print(str(poradi) + ". generace")
    generace = reprodukce(generace)
    print(generace)
    print("************************************************************************")

    # vyuzivame konstrukce generace, kdy vime, ze posledni prvek je maximalni v dane generaci
    maxnove = fce(dekod(generace[-1]))
    if max < maxnove:
        max = maxnove
        zmena = poradi
    poradi += 1

# LOGFITNESS = True
# fce(dekod("10010001001001010001"))
