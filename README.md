# Progetto: Stima di π tramite Metodo Monte Carlo e LCG

Questo repository contiene un'implementazione ad alte prestazioni in **Python puro** per la stima del valore di pi greco ($\pi$), sviluppata per la competizione del Laboratorio di Calcolo.

## 🚀 Obiettivo del Task
L'obiettivo è stimare il valore di $\pi$ analiticamente tramite una simulazione statistica: generare $N=100.000$ punti casuali in un quadrato unitario e determinare la frazione di essi che ricade all'interno del cerchio inscritto.

## 🛠️ Architettura Tecnica

### 1. Generatore Pseudo-Random (LCG)
Poiché l'uso di moduli esterni (come `random` o `numpy`) è vietato, è stato implementato un **Generatore Lineare Congruenziale** (Linear Congruential Generator). 
La formula ricorsiva utilizzata è:
$$x_{n+1} = (a \cdot x_n + c) \mod m$$

Sono stati adottati i parametri di *Numerical Recipes* (Knuth), che garantiscono un periodo pieno di $2^{32}$ (circa 4.3 miliardi di valori):
- **Moltiplicatore ($a$):** $1.664.525$
- **Incremento ($c$):** $1.013.904.223$
- **Modulo ($m$):** $2^{32}$

### 2. Metodo Monte Carlo e Analisi dell'Errore
La stima si basa sul rapporto geometrico tra l'area di un quarto di cerchio unitario e il quadrato unitario $[0,1] \times [0,1]$.
La condizione di appartenenza al cerchio per ogni punto $(x, y)$ è:
$$x^2 + y^2 \leq 1$$

Dal punto di vista statistico, l'errore del metodo Monte Carlo decresce con l'aumentare dei punti secondo la legge:
$$\epsilon \propto \frac{1}{\sqrt{N}}$$
Con $N=100.000$, la precisione attesa è nell'ordine di $10^{-3}$. Questa implementazione bilancia la necessità di precisione statistica con i vincoli di tempo computazionale.

## ⚡ Strategie di Ottimizzazione (Performance)
Il codice è stato ottimizzato per minimizzare l'overhead dell'interprete Python, ottenendo un tempo medio di circa **23.7 ms**:

*   **Method Caching:** L'istruzione `appendi = numeri.append` memorizza il riferimento al metodo in una variabile locale, eliminando la ricerca dell'attributo nell'oggetto lista a ogni iterazione (lookup costoso in Python).
*   **Branchless Programming:** Il contatore è aggiornato tramite `punti_dentro += (condizione)`. Sfruttando il fatto che i booleani sono sottoclassi di `int`, si evitano i rami condizionali (`if/else`) nel bytecode, linearizzando l'esecuzione.
*   **Efficienza Aritmetica:** L'uso di `x * x` è preferito a `x ** 2`. La moltiplicazione è un'operazione atomica gestita direttamente dalla ALU, mentre l'esponenziazione richiede una chiamata a funzioni più generiche e pesanti.
*   **Ottimizzazione della Distanza:** Il confronto avviene direttamente sulla somma dei quadrati rispetto a $1$, evitando il calcolo della radice quadrata (`math.sqrt`), operazione computazionalmente onerosa.

## ❓ FAQ Tecniche

**D: Perché usare due seed differenti (12345 e 67890)?**
**R:** Per garantire l'indipendenza statistica tra le coordinate $x$ e $y$. Utilizzare lo stesso seed porterebbe a punti distribuiti esclusivamente sulla diagonale, rendendo impossibile una corretta campionatura del piano.

**D: Perché normalizzare dividendo per $m$?**
**R:** L'LCG genera interi nell'intervallo $[0, m-1]$. La divisione riporta i valori nel range $[0, 1)$, necessario per la mappatura nel piano cartesiano unitario.

**D: Come viene gestito il jitter del dispositivo?**
**R:** Attraverso la minimizzazione delle istruzioni Python (bytecode compatto). Riducendo il carico di lavoro dell'interprete per singola operazione, si riduce la sensibilità della misura temporale al rumore di fondo del sistema operativo.

## 📈 Requisiti e Benchmark
- **Ambiente:** Python 3.x (IPython/Jupyter per `%timeit`)
- **Performance:** ~23.7 ms per $100.000$ punti.
- **Validazione:** I risultati ottenuti sono coerenti con la convergenza asintotica attesa per simulazioni stocastiche di questo tipo.
