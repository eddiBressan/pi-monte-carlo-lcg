def lcg(n, seed=1, a=1664525, c=1013904223, m=2**32):
    """Generatore Lineare Congruenziale.
    
    Parametri di Numerical Recipes (Knuth):
        a = 1664525
        c = 1013904223
        m = 2^32
    Periodo pieno = 2^32 ≈ 4.3 miliardi.
    
    Restituisce una lista di n numeri float in [0, 1).
    """
    numeri = []
    appendi = numeri.append
    x = seed

    for i in range(n):
        x = (a * x + c) % m
        appendi(x / m) #normalizzo per [0,1)

    return numeri
    

def stima_pi(N):
    """Stima pi con Monte Carlo. Restituisce il valore float di pi."""
    # Il vostro codice qui
    lista_x = lcg(N, 12345)
    lista_y = lcg(N, 67890)

    punti_dentro = 0

    for x,y in zip(lista_x, lista_y): #zip crea una sequenza di tuple [(x0,y0),(x1,y1),(x2,y2),...]
        """if x*x + y*y <= 1.0: #uso x*x invece di x^2 perché è più rapido
            punti_dentro += 1
        """
        punti_dentro += (x*x + y*y <= 1.0)
    return 4.0 * punti_dentro / N


N_punti = 100_000

risultato = stima_pi(N_punti)

#print(f"Stima di pi greco: {risultato}")