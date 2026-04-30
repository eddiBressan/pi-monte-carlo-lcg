# Stima di π tramite Metodo Monte Carlo e LCG

Questo progetto implementa un simulatore ad alte prestazioni in Python puro per la stima del valore di pi greco ($\pi$), sviluppato per la competizione del Laboratorio di Calcolo.

## 🚀 Obiettivo
L'obiettivo è stimare $\pi$ utilizzando $N=100.000$ punti generati casualmente all'interno di un quadrato unitario, calcolando il rapporto di quelli che cadono all'interno del cerchio inscritto.

## 🛠️ Architettura Tecnica

### 1. Generatore Pseudo-Random (LCG)
Invece di utilizzare librerie esterne, abbiamo implementato un **Generatore Lineare Congruenziale** basato sui parametri di *Numerical Recipes* (Knuth):
- **Moltiplicatore ($a$):** 1.664.525
- **Incremento ($c$):** 1.013.904.223
- **Modulo ($m$):** $2^{32}$

Per evitare correlazioni spaziali tra le coordinate $x$ e $y$ (che inficerebbero la stima), il sistema utilizza due istanze del generatore con **seed distinti**:
- `seed_x = 12345`
- `seed_y = 67890`

### 2. Algoritmo Monte Carlo
La stima si basa sul principio geometrico per cui il rapporto tra l'area di un cerchio e quella del quadrato in cui è inscritto è $\frac{\pi}{4}$. 
Il codice verifica per ogni punto $(x, y)$ la condizione:
$$x^2 + y^2 \leq 1$$

## ⚡ Strategie di Ottimizzazione (Performance)
Il codice è stato ottimizzato per minimizzare l'overhead dell'interprete Python, ottenendo un tempo di esecuzione di circa **23.7 ms**:

*   **Caching dei Metodi:** Abbiamo assegnato il metodo `.append` della lista a una variabile locale (`appendi`). Questo evita che Python debba cercare l'attributo nell'oggetto lista a ogni iterazione del ciclo (operazione costosa in cicli da $10^{5}$ iterazioni).
*   **Efficienza Aritmetica:** È stata utilizzata la moltiplicazione diretta `x * x` invece dell'operatore di potenza `x ** 2`, riducendo i cicli di clock necessari a livello di CPU.
*   **Branchless Programming:** Per il conteggio dei punti interni, abbiamo evitato l'uso di costrutti `if/else`, sfruttando la proprietà di Python per cui i booleani sono trattati come interi (`True = 1`). Questo approccio rende il bytecode più lineare e performante.
*   **Gestione del Jitter:** Le scelte di ottimizzazione sono state calibrate per bilanciare la velocità pura con la stabilità del sistema, garantendo risultati consistenti nonostante il jitter del dispositivo.

## 📈 Requisiti e Utilizzo
- **Linguaggio:** Python 3.x
- **Librerie:** Nessuna (Standard Library)
- **Esecuzione:** Il codice include il comando `%timeit` per il benchmarking in ambiente Jupyter/IPython.
```python
# Per eseguire la stima:
risultato = stima_pi(100_000)
