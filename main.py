def lcg(n, seed=1, a=1664525, c=1013904223, m=2**32):
    """Generatore Lineare Congruenziale."""
    numeri = []
    appendi = numeri.append
    x = seed

    for _ in range(n):
        x = (a * x + c) % m
        appendi(x / m)

    return numeri

def stima_pi(N):
    """Stima pi con Monte Carlo."""
    lista_x = lcg(N, 12345)
    lista_y = lcg(N, 67890)

    punti_dentro = 0
    for x, y in zip(lista_x, lista_y):
        punti_dentro += (x*x + y*y <= 1.0)
    
    return 4.0 * punti_dentro / N

# Esecuzione e test
N_punti = 100_000
risultato = stima_pi(N_punti)
#print(f"Stima di pi: {risultato}")

%timeit stima_pi(100_000)
