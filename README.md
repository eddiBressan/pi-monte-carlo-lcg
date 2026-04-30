# Progetto: Stima di π tramite Metodo Monte Carlo e LCG

Questo repository contiene un'implementazione ad alte prestazioni in **Python puro** per la stima del valore di pi greco ($\pi$), sviluppata per la competizione del Laboratorio di Calcolo.

## 🚀 Obiettivo del Task
L'obiettivo è stimare il valore di $\pi$ analiticamente tramite una simulazione statistica: generare $N=100.000$ punti casuali in un quadrato unitario e determinare la frazione di essi che ricade all'interno del cerchio inscritto.

## 🛠️ Architettura Tecnica

### 1. Generatore Pseudo-Random (LCG)
Poiché l'uso di moduli esterni (come `random` o `numpy`) è vietato, è stato implementato un **Generatore Lineare Congruenziale** (Linear Congruential Generator). 
La formula ricorsiva utilizzata è:
$$x_{n+1} = (a \cdot x_n + c) \mod m$$

Sono stati adottati i parametri di *Numerical Recipes* (Knuth), che garantiscono un periodo pieno di $2^{32}$:
- **Moltiplicatore ($a$):** $1.664.525$
- **Incremento ($c$):** $1.013.904.223$
- **Modulo ($m$):** $2^{32}$

### 2. Metodo Monte Carlo
La stima si basa sul rapporto tra l'area di un cerchio e quella del quadrato in cui è inscritto. In un sistema con raggio $r=1$ limitato al primo quadrante:
- Area Quadrato = $1 \times 1 = 1$
- Area Quarto di Cerchio = $\frac{\pi \cdot r^2}{4} = \frac{\pi}{4}$

La condizione di appartenenza al cerchio per ogni punto $(x, y)$ è:
$$x^2 + y^2 \leq 1$$

## ⚡ Strategie di Ottimizzazione (Performance)
Il codice è stato ottimizzato per minimizzare l'overhead dell'interprete Python e massimizzare il throughput dei dati, ottenendo un tempo di esecuzione di circa **23.7 ms**:

*   **Method Caching:** L'istruzione `appendi = numeri.append` memorizza il riferimento al metodo `.append()` in una variabile locale. Questo elimina la necessità per l'interprete di eseguire una ricerca dell'attributo nell'oggetto lista a ogni iterazione, risparmiando cicli di clock preziosi.
*   **Branchless Programming:** Invece di utilizzare un costrutto `if`, il contatore viene aggiornato tramite `punti_dentro += (condizione)`. In Python, i booleani sono sottoclassi di `int` (`True = 1`), e questo approccio riduce i salti condizionali nel bytecode, rendendo l'esecuzione più lineare.
*   **Efficienza Aritmetica:** È stata utilizzata la moltiplicazione diretta `x * x` invece dell'operatore di potenza `x ** 2`. L'esponenziazione è una funzione generica più pesante, mentre la moltiplicazione è un'operazione atomica gestita direttamente dalla ALU della CPU.
*   **Ottimizzazione della Distanza:** È stata evitata la funzione `math.sqrt()` confrontando direttamente la somma dei quadrati con $1$. Questo risparmia il calcolo della radice quadrata, operazione notoriamente onerosa.

## ❓ FAQ Tecniche

**D: Perché usare due seed differenti (12345 e 67890)?**
**R:** Per garantire l'indipendenza statistica tra le coordinate $x$ e $y$. Se usassimo lo stesso seed, otterremmo punti distribuiti solo sulla diagonale $x=y$, invalidando la natura bidimensionale della simulazione Monte Carlo.

**D: Perché dividere per $m$ alla fine del ciclo LCG?**
**R:** Il generatore restituisce numeri interi tra $0$ e $m-1$. La divisione normalizza i valori nel range $[0, 1)$, permettendo la corretta mappatura spaziale nel quadrato unitario.

**D: Come viene gestito il jitter del dispositivo?**
**R:** Il codice è scritto per essere il più compatto possibile a livello di istruzioni Python. Le ottimizzazioni adottate riducono il numero di operazioni che l'interprete deve gestire, minimizzando la varianza del tempo di esecuzione causata dal rumore di fondo del sistema operativo.

## 📈 Requisiti e Benchmark
- **Ambiente:** Python 3.x (IPython/Jupyter per `%timeit`)
- **Performance Media:** ~23.7 ms per $100.000$ punti.
- **Precisione:** Coerente con la convergenza $1/\sqrt{N}$ tipica del metodo Monte Carlo.
