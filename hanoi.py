def hanoi(n, start, cil, pomoc):
    if n > 0:
        hanoi(n - 1, start, pomoc, cil)
        print(f"Tohle je přesun {n} z {start} na {cil}")
        hanoi(n - 1, pomoc, cil, start)


hanoi(3, "A", "C", "B")
