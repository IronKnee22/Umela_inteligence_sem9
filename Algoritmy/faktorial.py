def factorial(n):
    if n == 0:
        return 1

    vysledek = n * factorial(n - 1)
    return vysledek


print(factorial(3))
