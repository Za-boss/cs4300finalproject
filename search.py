import random
import math
from itertools import combinations_with_replacement
from typing import TYPE_CHECKING, Any, Optional, Callable
from dataclasses import dataclass
if TYPE_CHECKING:
    from colony_simulation.wrapper import Colony_Wrapper
    from colony_simulation.colony import Colony

#This node class will need to change, it's just a template as of now
#May also need to include some sort of stats dataclass that stores the stats of the agent
@dataclass
class Node:
    state: "Colony"
    actions: Optional[tuple[tuple[str, int], ...]] = None
    parent: Optional["Node"] = None
class pf_stats:
    total_depth: int = 0
    average_depth: float = 0
    total_wins: int = 0
    total_runs: int = 0
    win_rate: float = 0.0
    nodes_generated: int = 0
class search_stats:
    attempts_needed: int = 0
    average_depth: float = 0
    success:  bool = False
    nodes_generated: int = 0
    nodes_explored: int = 0
def get_unique_combinations(
        actions: list[tuple[str, Callable, int]],
        possible_actions: int,
        available_energy: float
    ) -> list[tuple[tuple[str, Callable, int], ...]]:

    results: list[tuple[tuple[str, Callable, int], ...]] = []
    #the types for results might be a problem and the typechecker is being a little strange with them

    def combination_search(current_combo: list[tuple[str, Callable, int]], energy_left: float, start_index):
        if len(current_combo) == possible_actions:
            results.append(tuple(current_combo))
            return
        
        for i in range(start_index, len(actions)):
            action = actions[i]
            name, fn, cost = action

            if cost > energy_left and cost != 0:
                continue

            combination_search(current_combo + [action], energy_left - cost, i)

    combination_search([], available_energy, 0)
    return results

    # I need to check energy whenever I generate this as I currently check it in one go and that is not good

def default_dfs(problem: "Colony_Wrapper", attempts: int):
    stats = search_stats()
    total_depth = 0
    for i in range(attempts):
        stats.attempts_needed += 1
        frontier = [(Node(problem.initial_state), 0)]
        last_seen_state: "None | Colony" = None
        while frontier:
            node, depth = frontier.pop()
            stats.nodes_explored += 1
            last_seen_state = node.state
            if problem.goal_test(node.state):
                stats.success = True
                stats.average_depth = total_depth / stats.attempts_needed
                path = []
                while node:
                    path.append(node)
                    node = node.parent

                return (path[::-1], stats)
            chosen_action_list: list[tuple[str, Callable, int]] = []
            action_stats: list[tuple[str, int]] = []
            available_energy = node.state.energy
            for i in range(problem.actions_per_day):
                action_list = problem.get_actions(node.state, available_energy)
                #If the actions stay static for the entire run I might be able to just compute them at the start rather than computing it in this inner loop
                if action_list:
                    action = random.choice(action_list)
                    available_energy -= action[2]
                    chosen_action_list.append(action)
                    action_stats.append((action[0], action[2]))
                else:
                    break
            newState = problem.transition(node.state, chosen_action_list)
            stats.nodes_generated += 1
            problem.run_tick(newState)
            total_depth += 1
            if not newState.check_loss():
                frontier.append((Node(newState, tuple(action_stats), node), total_depth))
    stats.average_depth = total_depth / stats.attempts_needed
    return (None, stats)
def choose_state_temperature(
        scored: list[tuple[float, "Colony", list[tuple[str, int]]]], 
        temperature : float = 1.0):
    scores = [s[0] for s in scored]
    max_score = max(scores)
    exp_scores = [math.exp((s - max_score) / temperature) for s in scores]

    chosen_index = random.choices(range(len(scored)), weights=exp_scores, k=1)[0]
    return scored[chosen_index]

def heuristic_dfs(problem: "Colony_Wrapper", attempts: int):
    def get_state_key(state: "Colony"):
        return (
            new_state.current_day,
            new_state.population,
            new_state.food,
            new_state.energy,
            new_state.defense_capacity,
            tuple(sorted(b.building_name for b in new_state.buildings))
        )
    TEMPERATURE = 0.2
    stats = search_stats()
    total_depth = 0
    PRUNING_DEPTH = 3
    seen: set[tuple] = set()
    for _ in range(attempts):
        stats.attempts_needed += 1
        frontier = [(Node(problem.initial_state), 0)]
        while frontier:
            node, depth = frontier.pop()
            stats.nodes_explored += 1
            
            if problem.goal_test(node.state):
                stats.success = True
                stats.average_depth = total_depth / stats.attempts_needed
                path = []
                while node:
                    path.append(node)
                    node = node.parent                
                return (path[::-1], stats)
            
            available_energy = node.state.energy
            action_list = problem.get_actions(node.state, available_energy)
            action_combinations = get_unique_combinations(action_list, problem.actions_per_day, available_energy)

            scored: list[tuple[float, "Colony", list[tuple[str, int]]]] = [] 
            action_stats: list[tuple[str, int]] = []

            for combination in action_combinations:
                new_state = problem.transition(node.state, list(combination))
                action_stats = [(name, cost) for (name, _, cost) in combination]


                state_key = get_state_key(new_state)

                if state_key in seen:
                    continue
                
                stats.nodes_generated += 1
                scored.append((problem.heuristic(new_state), new_state, action_stats))
            if not scored:
                break

            chosen_score, chosen_state, chosen_actions = choose_state_temperature(scored, TEMPERATURE)

            if total_depth >= PRUNING_DEPTH:
                chosen_key = get_state_key(chosen_state)
                seen.add(chosen_key)
            problem.run_tick(chosen_state)
            total_depth += 1
            if not chosen_state.check_loss():
                frontier.append((Node(chosen_state, tuple(chosen_actions), node), total_depth))

    stats.average_depth = total_depth / stats.attempts_needed
    return (None, stats)
#This function attempts to roughly determine how many realistic win conditions there are
def percentage_fuzzing(problem: "Colony_Wrapper", attempts: int=100000) -> "pf_stats": 
    stats = pf_stats()

    for _ in range(attempts):
        frontier = [(Node(problem.initial_state), 0)]
        total_depth = 0
        stats.total_runs += 1
        while frontier:
            node, depth = frontier.pop()
            if problem.goal_test(node.state):
                stats.total_wins += 1
                break
            chosen_action_list: list[tuple[str, Callable, int]] = []
            action_stats: list[tuple[str, int]] = []
            available_energy = node.state.energy
            for i in range(problem.actions_per_day):
                action_list = problem.get_actions(node.state, available_energy)
                if action_list:
                    action = random.choice(action_list)
                    available_energy -= action[2]
                    chosen_action_list.append(action)
                    action_stats.append((action[0], action[2]))
                else:
                    break
                    #This might be entirely redundant because the loop only runs an amount equal to the actions per day
            newState = problem.transition(node.state, chosen_action_list)
            problem.run_tick(newState)
            total_depth += 1
            if not newState.check_loss():
                frontier.append((Node(newState, tuple(action_stats), node), total_depth))
                stats.nodes_generated += 1
                stats.total_depth += 1
    stats.win_rate = stats.total_wins / stats.total_runs
    stats.average_depth = stats.total_depth / stats.total_runs
    return stats
        