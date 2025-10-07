import sys

import pygame

# --- 1. NASTAVENÍ ---

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
SIRKA_OKNA, VYSKA_OKNA = 800, 600
okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
pygame.display.set_caption("Hanojské věže - Animace")

# Barvy (R, G, B)
BARVA_POZADI = (30, 30, 40)
BARVA_KOLIKU = (100, 80, 70)
BARVA_ZAKLADNY = (60, 50, 40)
BARVY_DISKU = [
    (220, 90, 90),
    (220, 160, 90),
    (220, 220, 90),
    (160, 220, 90),
    (90, 220, 90),
    (90, 220, 160),
    (90, 220, 220),
    (90, 160, 220),
    (90, 90, 220),
    (160, 90, 220),
]

# Počet disků (můžeš změnit)
POCET_DISKU = 10

# Geometrie
VYSKA_DISKU = 25
MAX_SIRKA_DISKU = 200
MIN_SIRKA_DISKU = 50
VYSKA_KOLIKU = 300
SIRKA_KOLIKU = 15

# Výpočet pozic kolíků
pozice_koliku = [(SIRKA_OKNA / 4), (SIRKA_OKNA / 2), (SIRKA_OKNA * 3 / 4)]
Y_ZAKLADNA = VYSKA_OKNA - 100

# --- 2. LOGIKA HRY (MOZEK) ---


def hanoi(n, start, cil, pomocny, seznam_tahu):
    """Rekurzivní funkce, která generuje a ukládá seznam tahů."""
    if n > 0:
        hanoi(n - 1, start, pomocny, cil, seznam_tahu)
        # Místo printu ukládáme tah do seznamu
        seznam_tahu.append((start, cil))
        hanoi(n - 1, pomocny, cil, start, seznam_tahu)


# --- 3. POMOCNÉ A KRESLÍCÍ FUNKCE ---

# Vytvoření datové struktury pro kolíky a disky
koliky = [[] for _ in range(3)]  # 3 prázdné seznamy pro 3 kolíky
for i in range(POCET_DISKU, 0, -1):
    koliky[0].append(i)  # Naplníme první kolík disky od největšího po nejmenší


def vypocitej_pozici_disku(kolik_idx, pozice_v_zasobniku, disk_cislo):
    """Vypočítá x, y souřadnice a rozměry pro daný disk."""
    sirka_disku = MIN_SIRKA_DISKU + (MAX_SIRKA_DISKU - MIN_SIRKA_DISKU) * (
        (disk_cislo - 1) / (POCET_DISKU - 1)
    )
    x = pozice_koliku[kolik_idx] - sirka_disku / 2
    y = Y_ZAKLADNA - (pozice_v_zasobniku + 1) * VYSKA_DISKU
    return pygame.Rect(x, y, sirka_disku, VYSKA_DISKU)


def nakresli_scenu():
    """Vykreslí celou herní scénu - pozadí, základnu, kolíky a disky."""
    # Pozadí
    okno.fill(BARVA_POZADI)

    # Základna
    pygame.draw.rect(
        okno, BARVA_ZAKLADNY, (0, Y_ZAKLADNA, SIRKA_OKNA, VYSKA_OKNA - Y_ZAKLADNA)
    )

    # Kolíky
    for x in pozice_koliku:
        pygame.draw.rect(
            okno,
            BARVA_KOLIKU,
            (
                x - SIRKA_KOLIKU / 2,
                Y_ZAKLADNA - VYSKA_KOLIKU,
                SIRKA_KOLIKU,
                VYSKA_KOLIKU,
            ),
        )

    # Disky
    for idx_koliku, zasobnik in enumerate(koliky):
        for idx_v_zasobniku, cislo_disku in enumerate(zasobnik):
            rect = vypocitej_pozici_disku(idx_koliku, idx_v_zasobniku, cislo_disku)
            pygame.draw.rect(okno, BARVY_DISKU[cislo_disku - 1], rect, border_radius=10)


# --- 4. ANIMAČNÍ FUNKCE (SVALY) ---


def animuj_presun(start_idx, cil_idx, rychlost=500):
    """Zanimuje přesun vrchního disku ze startovního na cílový kolík."""

    # 1. Příprava
    disk_k_presunu = koliky[start_idx].pop()
    start_rect = vypocitej_pozici_disku(
        start_idx, len(koliky[start_idx]), disk_k_presunu
    )
    cil_rect = vypocitej_pozici_disku(cil_idx, len(koliky[cil_idx]), disk_k_presunu)

    # Současné souřadnice disku, který animujeme
    x, y = start_rect.topleft
    sirka, vyska = start_rect.size

    # 2. Animace nahoru
    while y > 50:
        y -= rychlost
        nakresli_scenu()
        pygame.draw.rect(
            okno,
            BARVY_DISKU[disk_k_presunu - 1],
            (x, y, sirka, vyska),
            border_radius=10,
        )
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # 3. Animace do strany
    cílové_x = cil_rect.left
    while x != cílové_x:
        x += rychlost if cílové_x > x else -rychlost
        # Ošetření, abychom nepřeskočili cíl
        if abs(x - cílové_x) < rychlost:
            x = cílové_x

        nakresli_scenu()
        pygame.draw.rect(
            okno,
            BARVY_DISKU[disk_k_presunu - 1],
            (x, y, sirka, vyska),
            border_radius=10,
        )
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # 4. Animace dolů
    cílové_y = cil_rect.top
    while y != cílové_y:
        y += rychlost
        # Ošetření, abychom nepřeskočili cíl
        if abs(y - cílové_y) < rychlost:
            y = cílové_y

        nakresli_scenu()
        pygame.draw.rect(
            okno,
            BARVY_DISKU[disk_k_presunu - 1],
            (x, y, sirka, vyska),
            border_radius=10,
        )
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # 5. Aktualizace datové struktury
    koliky[cil_idx].append(disk_k_presunu)


# --- 5. HLAVNÍ ČÁST PROGRAMU ---

# Vygenerujeme si všechny potřebné tahy
mapovani_koliku = {"A": 0, "B": 1, "C": 2}
seznam_tahu_abc = []
hanoi(POCET_DISKU, "A", "C", "B", seznam_tahu_abc)

# Převedeme tahy z "A","B","C" na indexy 0,1,2
seznam_tahu_idx = [
    (mapovani_koliku[start], mapovani_koliku[cil]) for start, cil in seznam_tahu_abc
]

# Hlavní herní smyčka
running = True
tah_ke_zpracovani = 0

while running:
    # Zpracování událostí (např. zavření okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vykreslení aktuální scény
    nakresli_scenu()
    pygame.display.flip()  # Aktualizuje obrazovku

    # Zpracování a animace jednoho tahu
    if tah_ke_zpracovani < len(seznam_tahu_idx):
        start, cil = seznam_tahu_idx[tah_ke_zpracovani]
        # time.sleep(0.1)  # Krátká pauza před každým tahem
        animuj_presun(start, cil)
        tah_ke_zpracovani += 1

# Ukončení Pygame
pygame.quit()
sys.exit()
