# Colony Management AI Simulation

This project simulates a resource management colony where an AI agent must survive for a set number of days (default 31) by managing resources (Food, Energy, Population, Defense) and constructing buildings.

The project consists of three main components:
1.  **Training (`train.py`):** Uses a Genetic Algorithm to evolve optimal heuristic weights.
2.  **Benchmarking (`benchmark.py`):** Rigorously tests trained weights against a baseline and a control group (Default DFS).
3.  **Simulation (`run.py`):** Visualizes specific runs and executes the agent in real-time.

---

## 1. Workflow Overview

To build the best AI agent, follow this workflow:

1.  **Train:** Run `train.py` to evolve a set of weights for the simulation to use.
2.  **Benchmark:** Use `benchmark.py` in order to check the accuracy of the given weights.
3.  **Visualize:** Use `run.py` with your weight file to watch the timeline of a specific simulation.


---

## 2. Training New Agents (`train.py`)

The `train.py` script uses a genetic algorithm to tune the `Heuristic_Values`. It generates a population of random agents, evaluates them against random scenarios, and mutates the winners over several generations.

### Usage
```bash
# Train for 20 generations, with 50 agents per generation
# Save the best resulting weights to 'my_best_weights.txt'
python3 train.py --generations 20 --population-size 50 --output-file my_best_weights.txt
````

### Arguments

| Argument | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--output-file` | `--of` | **Required** | The file path to save the winning heuristic weights. |
| `--generations` | `--g` | `10` | Number of generations to evolve the agents. |
| `--population-size` | `--ps` | `50` | Number of agents in every generation. |
| `--num-simulations` | `--ns` | `10` | How many random scenarios each agent attempts per generation (higher = more robust). |
| `--top-k` | `--tk` | `5` | How many top agents survive to reproduce in the next generation. |

-----

## 3\. Benchmarking (`benchmark.py`)

Once you have a weight file, use `benchmark.py` to audit it. This script runs a "3-Way Handshake" on identical seeds:

1.  **Candidate:** Your trained weights.
2.  **Baseline:** Default hardcoded weights (or a second file).
3.  **Control:** Default DFS (Blind search).

### Usage

```bash
# Compare 'my_best_weights.txt' against the defaults over 50 scenarios
python3 benchmark.py --candidate my_best_weights.txt --scenarios 50
```

### Arguments

| Argument | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--candidate` | `-c` | **Required** | Path to the weight file you want to test. |
| `--baseline` | `-b` | `None` | Path to a second weight file to compare against. If omitted, uses default hardcoded weights. |
| `--scenarios` | `-n` | `50` | Number of random seeds (universes) to test. |
| `--node-expansions`| `--nea`| `500` | Max nodes the search is allowed to explore. |
| `--seed` | `-s` | Random | Master seed for the benchmark batch. |

-----

## 4\. Running & Visualization (`run.py`)

The `run.py` script is used to execute a single agent or fuzz the simulation. It is best used for debugging specific seeds or watching the decision-making process.

### Usage

**Run through a scenario with an algorithm and see the results**

```bash
python3 run.py --algo heuristic_dfs --wf my_best_weights.txt --seed 12345 --dt True
```

**Run the default "blind" DFS (Control):**

```bash
python3 run.py --algo default_dfs
```

### Arguments

| Argument | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--algorithm` | `--algo` | `default_dfs` | Choose `default_dfs`, `heuristic_dfs`, or `percentage_fuzzing`. |
| `--weight-file` | `--wf` | `None` | Path to a file containing heuristic weights. Uses internal defaults if blank. |
| `--display-timeline`| `--dt` | `False` | Prints the day-by-day actions, resources, and events. |
| `--node-expansions-allowed`| `--nea`| `500` | Max search depth/nodes for DFS algorithms. |
| `--actions-per-day`| `--apd` | `3` | Actions allowed per day (Min 1, Max 6). |
| `--seed` | `--s` | Random | RNG seed. |
| `--run-count` | `--rc` | `10` | Only used for `percentage_fuzzing`. |

-----

## 5\. Heuristics Explanation

The AI makes decisions based on the following weighted values (found in `Heuristic_Values`). These are the parameters optimized by `train.py`:

  * **Weights (`w_`):** How much the agent values having raw resources (Food, Energy, Defense, Population).
  * **Targets (`_target`):** The specific amount of a resource the agent aims to maintain.
