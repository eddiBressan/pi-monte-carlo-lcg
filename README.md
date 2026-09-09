# Project: π Estimation via Monte Carlo Method and LCG

This repository contains a high-performance, **pure Python** implementation for estimating the value of pi ($\pi$), developed for an academic scientific computing competition.

## 🚀 Task Objective
The objective is to estimate the value of $\pi$ analytically via statistical simulation: generate $N = 100,000$ pseudorandom points inside a unit square and determine the fraction of points that fall within the inscribed quarter unit circle.

## 🛠️ Technical Architecture

### 1. Pseudorandom Number Generator (LCG)
External modules (such as `random` or `numpy`) are not permitted, so a custom **Linear Congruential Generator** (LCG) was implemented.
The recurrence relation is:
$$x_{n+1} = (a \cdot x_n + c) \mod m$$

Parameters from *Numerical Recipes* (Knuth) are used to ensure a full period of $2^{32}$ (~4.3 billion states):
- **Multiplier ($a$):** $1,664,525$
- **Increment ($c$):** $1,013,904,223$
- **Modulus ($m$):** $2^{32}$

### 2. Monte Carlo Method and Error Analysis
The estimation relies on the geometric ratio between the area of a quarter unit circle and the unit square $[0,1] \times [0,1]$.
The condition for a point $(x, y)$ falling inside the circle is:
$$x^2 + y^2 \leq 1$$

Statistically, the error associated with the Monte Carlo method scales inversely with the square root of the sample size:
$$\epsilon \propto \frac{1}{\sqrt{N}}$$
With $N = 100,000$, the expected precision is on the order of $10^{-3}$, balancing statistical convergence with strict execution time constraints.

## ⚡ Performance Optimization Strategies
The codebase is optimized to minimize CPython interpreter overhead, achieving an average runtime of approximately **23.7 ms**:

*   **Method Caching:** `appendi = numeri.append` stores the bound method reference in a local variable, avoiding costly attribute lookups on the list object during each iteration.
*   **Branchless Execution:** The accumulator updates via `punti_dentro += (condition)`. Since booleans inherit from `int` in Python, this eliminates conditional jump instructions (`if/else`) in the bytecode, maintaining linear execution flow.
*   **Arithmetic Efficiency:** Using `x * x` instead of `x ** 2` leverages direct ALU multiplication without the overhead of the generic `POW` opcode.
*   **Euclidean Distance Optimization:** The condition tests the sum of squares directly against $1$, bypassing expensive square root evaluations (`math.sqrt`).

## ❓ Technical FAQ

**Q: Why use two distinct seeds (12345 and 67890)?**  
**A:** To preserve statistical independence between the $x$ and $y$ coordinate streams. Using the same seed would restrict points to the main diagonal, preventing valid planar sampling.

**Q: Why normalize by dividing by $m$?**  
**A:** The LCG outputs raw integers in the interval $[0, m-1]$. Dividing by $m$ scales the values to $[0, 1)$, matching the unit square domain.

**Q: How is execution jitter mitigated?**  
**A:** By reducing bytecode complexity and instruction count per iteration, minimizing the interpreter's susceptibility to system-level scheduling noise during timing benchmarks.

## 📈 Requirements and Benchmarks
- **Environment:** Python 3.x (IPython / Jupyter for `%timeit`)
- **Performance:** ~23.7 ms for $100,000$ points
- **Validation:** Results align with asymptotic theoretical convergence for stochastic simulations of this scale.
