#!/usr/bin/env python3
import argparse
import random
import time
from dataclasses import dataclass
from statistics import mean

from typing import Callable

# Import necessary components
from search import heuristic_dfs, default_dfs
from colony_simulation.colony import Colony
from colony_simulation.wrapper import Colony_Wrapper
from colony_simulation.default_buildings import ALL_BUILDINGS, farm, nuclear_reactor
from colony_simulation.default_events import ALL_EVENTS

# Reusing specific logic from run.py
from run import (
    setup_simulation, 
    make_heuristic_values, 
    read_heuristic_weights, 
    Heuristic_Values
)

@dataclass
class SimulationResult:
    seed: int
    success: bool
    depth: int
    nodes_generated: int
    execution_time: float

def run_single_scenario(
    seed: int, 
    heuristic_weights: Heuristic_Values, 
    algorithm_func: Callable,
    node_limit: int, 
    actions_per_day: int,
    goal_days: int
) -> SimulationResult:
    
    random.seed(seed)
    colony, buildings = setup_simulation(goal_days)
    
    # Wrapper always needs weights, even if default_dfs ignores them
    wrapper = Colony_Wrapper(colony, buildings, heuristic_weights)
    wrapper.actions_per_day = actions_per_day
    wrapper.goal_day = goal_days

    start_time = time.time()
    # Run the specific algorithm passed in (heuristic_dfs or default_dfs)
    path, stats = algorithm_func(wrapper, node_expansions_allowed=node_limit)
    end_time = time.time()

    return SimulationResult(
        seed=seed,
        success=stats.success,
        depth=len(path) if path else 0,
        nodes_generated=stats.nodes_generated,
        execution_time=end_time - start_time
    )

def print_summary(title: str, results: list[SimulationResult]):
    total = len(results)
    wins = [r for r in results if r.success]
    if not results: return

    win_rate = (len(wins) / total) * 100
    avg_nodes = mean([r.nodes_generated for r in results])
    avg_time = mean([r.execution_time for r in results])
    avg_depth = mean([r.depth for r in wins]) if wins else 0.0

    print(f"--- {title} ---")
    print(f"Win Rate:        {win_rate:.2f}% ({len(wins)}/{total})")
    print(f"Avg Depth (Wins): {avg_depth:.2f}")
    print(f"Avg Nodes Gen:   {avg_nodes:.1f}")
    print(f"Avg Time:        {avg_time:.4f}s")

def main():
    parser = argparse.ArgumentParser(description="Benchmark heuristic weights against baseline and default DFS.")
    parser.add_argument('--candidate', '-c', type=str, required=True, help="Path to the new heuristic weights.")
    parser.add_argument('--baseline', '-b', type=str, required=False, help="Path to baseline weights (optional).")
    parser.add_argument('--scenarios', '-n', type=int, default=50, help="Number of scenarios to run.")
    parser.add_argument('--node-expansions', '--nea', type=int, default=500)
    parser.add_argument('--actions-per-day', '--apd', type=int, default=3)
    parser.add_argument('--seed', '-s', type=int, help="Master seed.")

    args = parser.parse_args()

    # 1. Setup Seeds
    master_seed = args.seed if args.seed else random.randrange(10000000)
    random.seed(master_seed)
    scenario_seeds = [random.randrange(100000000) for _ in range(args.scenarios)]
    
    print(f"Master Seed: {master_seed}")
    print(f"Running {args.scenarios} scenarios...")

    # 2. Load Weights
    cand_weights = read_heuristic_weights(args.candidate)
    
    if args.baseline:
        base_weights = read_heuristic_weights(args.baseline)
        base_name = "Baseline"
    else:
        base_weights = make_heuristic_values()
        base_name = "Default Weights"

    results = {"Cand": [], "Base": [], "Dflt": []}
    
    # Table Header
    print(f"\n{'#':<3} | {'Cand':<8} | {'Base':<8} | {'Default':<8} | {'Nodes (Cand vs Base)':<20}")
    print("-" * 60)

    # 3. Execution Loop
    for i, seed in enumerate(scenario_seeds):
        # Run Candidate (Heuristic DFS)
        r_c = run_single_scenario(seed, cand_weights, heuristic_dfs, args.node_expansions, args.actions_per_day, 31)
        results["Cand"].append(r_c)

        # Run Baseline (Heuristic DFS)
        r_b = run_single_scenario(seed, base_weights, heuristic_dfs, args.node_expansions, args.actions_per_day, 31)
        results["Base"].append(r_b)

        # Run Default DFS (Control Group)
        # We pass base_weights to wrapper initialization, but default_dfs likely ignores them
        r_d = run_single_scenario(seed, base_weights, default_dfs, args.node_expansions, args.actions_per_day, 31)
        results["Dflt"].append(r_d)

        # Formatting Output
        stat_c = "WIN" if r_c.success else "LOSS"
        stat_b = "WIN" if r_b.success else "LOSS"
        stat_d = "WIN" if r_d.success else "LOSS"
        
        # Calculate efficiency difference (Negative is better for candidate)
        diff = r_c.nodes_generated - r_b.nodes_generated
        diff_str = f"{diff:+}" if r_c.success and r_b.success else "N/A"

        print(f"{i+1:<3} | {stat_c:<8} | {stat_b:<8} | {stat_d:<8} | {diff_str:<20}")

    print("\n" + "="*30)
    print("FINAL STATISTICS")
    print("="*30)
    
    print_summary("CANDIDATE (Heuristic DFS)", results["Cand"])
    print("")
    print_summary(f"BASELINE ({base_name})", results["Base"])
    print("")
    print_summary("CONTROL (Default DFS)", results["Dflt"])

if __name__ == "__main__":
    main()