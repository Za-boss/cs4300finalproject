#!/usr/bin/env python3
#This file trains the heuristics of the model and after doing so writes it to an outfile
import random
import argparse
from dataclasses import dataclass, fields
from colony_simulation.colony import Colony
from colony_simulation.building import Building
from colony_simulation.wrapper import Colony_Wrapper
from colony_simulation.default_buildings import *
from colony_simulation.default_events import *
from search import heuristic_dfs, default_dfs, search_stats, Node
# Importing necessary setup functions and data structures from run.py
from run import Heuristic_Values, setup_simulation

def generate_random_agent(weight_min: float, weight_max: float) -> Heuristic_Values:
    return Heuristic_Values(
        w_food=random.uniform(weight_min, weight_max),
        w_energy=random.uniform(weight_min, weight_max),
        w_defense=random.uniform(weight_min, weight_max),
        w_population=random.uniform(weight_min, weight_max),

        food_target_base=random.uniform(300.0, 800.0),
        energy_prod_target=random.uniform(200.0, 600.0),
        defense_target=random.uniform(200.0, 800.0), # Needs to go high for massive raids
        population_target=random.uniform(100.0, 400.0),
        efficiency_target=random.uniform(0.5, 0.95),

        below_efficiency_population_w=random.uniform(weight_min, weight_max),
        below_food_target_food_w=random.uniform(weight_min, weight_max),
        below_energy_target_energy_w=random.uniform(weight_min, weight_max)
    )

def mutate_agent(agent: Heuristic_Values, weight_min: float, weight_max: float, mutation_rate: float = 0.3) -> Heuristic_Values:
    """Creates a new agent by slightly modifying the weights of a parent agent."""
    new_kwargs = {}
    
    # Different mutation strengths for different types of values
    weight_mutation_strength = 1.0 
    target_mutation_strength = 50.0  # Targets need bigger jumps (e.g. Defense 300 -> 350)
    percent_mutation_strength = 0.1 # For efficiency target (0.0 - 1.0)

    for field in fields(agent):
        name = field.name
        value = getattr(agent, name)
        
        if random.random() < mutation_rate:
            if "w_" in name or "_w" in name:
                # Mutate Weights (1.0 - 7.5 range)
                change = random.uniform(-weight_mutation_strength, weight_mutation_strength)
                new_value = max(weight_min, min(weight_max, value + change))
                new_kwargs[name] = new_value
            
            elif "efficiency_target" in name:
                # Mutate Efficiency (0.0 - 1.0 range)
                change = random.uniform(-percent_mutation_strength, percent_mutation_strength)
                new_value = max(0.1, min(1.0, value + change))
                new_kwargs[name] = new_value

            elif "target" in name:
                # Mutate Targets (100 - 1000 range)
                change = random.uniform(-target_mutation_strength, target_mutation_strength)
                # Ensure targets don't go negative or absurdly high
                new_value = max(50.0, min(2000.0, value + change))
                new_kwargs[name] = new_value
            else:
                new_kwargs[name] = value
        else:
            new_kwargs[name] = value
            
    return Heuristic_Values(**new_kwargs)

def evaluate_baseline(seeds: list[int]) -> tuple[float, float]:
    wins = 0
    avg_depth = 0
    node_expansion_limit = 300
    
    dummy_agent = generate_random_agent(1.0, 1.0)

    for seed in seeds:
        random.seed(seed)
        
        GOAL_DAYS = 31
        colony, buildings = setup_simulation(GOAL_DAYS)
        
        wrapper = Colony_Wrapper(colony, buildings, heuristic_values=dummy_agent)
        wrapper.actions_per_day = 3 
        wrapper.goal_day = GOAL_DAYS
        
        path, stats = default_dfs(wrapper, node_expansions_allowed=node_expansion_limit)
        
        if stats.success:
            wins += 1
        avg_depth += len(path)
        
            
    win_rate = wins / len(seeds)
    
    return (win_rate, avg_depth / len(seeds))

def evaluate_agent(agent: Heuristic_Values, seeds: list[int]) -> tuple[float, float]:
    wins = 0
    avg_depth = 0
    node_expansion_limit = 1500
    
    for seed in seeds:

        random.seed(seed)
        
        GOAL_DAYS = 31
        colony, buildings = setup_simulation(GOAL_DAYS)
        
        wrapper = Colony_Wrapper(colony, buildings, heuristic_values=agent)
        wrapper.actions_per_day = 3 
        wrapper.goal_day = GOAL_DAYS
        
        path, stats = heuristic_dfs(wrapper, node_expansion_limit)
        
        if stats.success:
            wins += 1
        avg_depth += len(path)
            
    return (wins / len(seeds), avg_depth / len(seeds))

def save_best_agent(agent: Heuristic_Values, filepath: str):
    try:
        with open(filepath, 'w') as f:
            for field in fields(agent):
                name = field.name
                value = getattr(agent, name)
                f.write(f"{name} | {value}\n")
        print(f"Successfully saved best weights to {filepath}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Train heuristic weights for the colony simulation AI.")
    parser.add_argument('--num-simulations', '--ns', required=False, type=int, default=10, help="The number of different simulations to run per agent")
    parser.add_argument('--generations', '--g', required=False, type=int, default=10, help="The number of generations to train for")
    parser.add_argument('--population-size', '--ps', required=False, type=int, default=50, help="The number of agents to run in each generation")
    parser.add_argument('--top-k', '--tk', required=False, type=int, default=5, help="The number of agents to select for each generation")
    parser.add_argument('--output-file', '--of', required=True, type=str,help="The file to write the results to")
    args = parser.parse_args()
    
    WEIGHT_MIN = 0.25
    WEIGHT_MAX = 7.5

    num_simulations = args.num_simulations
    generations = args.generations
    population_size = args.population_size
    top_k = args.top_k
    output_file = args.output_file
    population = [generate_random_agent(WEIGHT_MIN, WEIGHT_MAX) for _ in range(population_size)]
    
    print(f"Starting training: {generations} generations, pop size {population_size}, {num_simulations} sims/agent.")
    
    for gen in range(generations):
        seeds = [seed for seed in random.sample(range(10000000), num_simulations)]

        scored_population = []
        base_win, base_depth = evaluate_baseline(seeds)
      
        for i, agent in enumerate(population):
            fitness = evaluate_agent(agent, seeds)
            scored_population.append((fitness, agent))
        
        scored_population.sort(key=lambda x: x[0], reverse=True)
        
        best_stats = scored_population[0][0]
        best_win_rate, best_avg_depth = best_stats
        print(f"Gen {gen+1}/{generations} | Best Win Rate: {best_win_rate * 100:.1f}% | Avg Depth: {best_avg_depth:.1f}")       
        print(f"Baseline: {base_win * 100:.1f}% | Avg Depth: {base_depth:.1f}") 
        next_generation = [agent for score, agent in scored_population[:top_k]]
        
        while len(next_generation) < population_size:
            parent = random.choice(next_generation[:top_k])
            child = mutate_agent(parent, WEIGHT_MIN, WEIGHT_MAX)
            next_generation.append(child)
            
        population = next_generation

    best_agent = population[0]
    
    print("Training complete.")
    save_best_agent(best_agent, output_file)

if __name__ == "__main__":
    main()