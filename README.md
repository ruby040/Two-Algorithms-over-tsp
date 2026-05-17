# TSP Solver — Simulated Annealing & Firefly Algorithm

## What is this project?

This project implements two different metaheuristic algorithms to solve the Traveling Salesman Problem (TSP). The first is Simulated Annealing (SA) and the second is the Firefly Algorithm (FA). Both were tested on two well-known benchmark instances from TSPLIB: `eil51` and `pr264`.

---

## Files

| File | Description |
|---|---|
| `sa_tsp.py` | Simulated Annealing implementation |
| `firefly_tsp.py` | Firefly Algorithm implementation |
| `data/eil51.tsp` | First dataset — 51 cities |
| `data/pr264.tsp` | Second dataset — 264 cities |

---

## How to Run

Make sure Python is installed, then run:

```bash
# Run Simulated Annealing
python sa_tsp.py

# Run Firefly Algorithm
python firefly_tsp.py
```

> Note: Run the scripts from the same folder that contains the `data/` directory so the `.tsp` files are read correctly.

---

## Parameters

### Simulated Annealing
- **Initial Temperature:** 100  
- **Alpha (cooling rate):** 0.99  
- **Max Iterations:** 500  
- **Stopping condition:** When temperature drops below 0.1 or iterations are exhausted

### Firefly Algorithm
- **Number of Fireflies:** 20  
- **Max Iterations:** 500  
- **Alpha:** 0.5 (controls the balance between exploration and exploitation)

---

## Neighbor Generation

In SA, we use a **partial 2-opt move** — a random position in the path is selected and a segment of up to 6 cities is reversed. It follows the same logic as 2-opt but applied locally.

In the Firefly Algorithm, two types of moves are used:
- **Random swap** for exploration (when `random < alpha`)
- **Segment copy from a brighter firefly** for exploitation

---

## How It Works (Simplified)

**Simulated Annealing:**
1. Start with a random tour
2. Generate a neighbor by reversing a segment
3. If better → accept; if worse → accept with probability `e^(ΔE/T)`
4. Cool down the temperature by multiplying by alpha
5. Repeat until iterations run out or temperature is too low

**Firefly Algorithm:**
1. Start with 20 fireflies, each with a random tour
2. Each firefly moves toward brighter ones (higher brightness = shorter distance)
3. Movement is either a random swap or copying a segment from the better firefly
4. Track the best tour found throughout the run

---

## Seeds

Each algorithm was run **20 times** using seeds 1 through 20 to ensure reproducible and statistically reliable results.

---

## Requirements

```
python >= 3.7
numpy
math (built-in)
random (built-in)
time (built-in)
```

Install numpy if not already installed:
```bash
pip install numpy
```

---

## Note

The datasets are taken from TSPLIB, a well-known benchmark library for TSP problems. The optimal solution for `eil51` is ~426 and for `pr264` is ~49135 — you can use these as a reference to evaluate your results.
