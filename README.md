# Run Instructions

The colony simulation is executed via the main script, `run.py`. It uses command-line arguments to select the AI algorithm, adjust its parameters, and control the output detail.

### Basic Execution

To run the simulation with the default settings (Default DFS, 100 attempts, 3 actions per day):

```bash
python3 run.py
```

-----

## Command Line Arguments

The following arguments can be used to customize the simulation run:

| Argument | Short Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--algorithm` | `--algo` | string | `default_dfs` | **The search algorithm to use.** Valid choices are: `default_dfs`, `heuristic_dfs`, and `percentage_fuzzing`. |
| `--run_count` | `--rc` | integer | `10` | **Total runs for fuzzing.** Only used when `--algorithm` is set to `percentage_fuzzing`. |
| `--attempt_count` | `--ac` | integer | `100` | **Maximum search attempts.** The maximum number of attempts at solving the problem the Depth-First Search (DFS) algorithms (`default_dfs`, `heuristic_dfs`) are allowed to execute. |
| `--seed` | `--s` | integer | Random | The seed for the random number generator. If left blank, a random seed is generated and printed. Use this to reproduce a specific simulation run. |
| `--display_timeline`| `--dt` | boolean | `False` | Whether or not to display the detailed day-by-day timeline, including the AI's actions, resource changes, and triggered events. |
| `--actions-per-day`| `--apd` | integer | `3` | The number of actions the agent is allowed to take each day. **Clamped** between a minimum of `1` and a maximum of `6`. |

-----

## Usage Examples

**1. Running the Heuristic DFS Algorithm:**

```bash
python3 run.py --algo heuristic_dfs
```

**2. Viewing a Detailed Timeline of a Specific Run:**
Use this to analyze the exact path the agent took. The seed ensures reproducibility.

```bash
python3 run.py --seed 420420 --dt True
```

**3. Running the Percentage Fuzzing Algorithm:**
The `--rc` argument dictates the number of times the random simulation is run to determine a rough overall win rate for a given scenario.

```bash
python3 run.py --algo percentage_fuzzing --rc 500
```

**4. Adjusting the Agent's Daily Actions:**
Allows the agent to take up to 6 actions per day instead of the default 3.

```bash
python3 run.py --actions-per-day 6
```

**5. Increasing Search Attempts:**
Give the default DFS or heuristic DFS a higher amount of attempts to potentially find a solution for a difficult seed.

```bash
python3 run.py --ac 500
```