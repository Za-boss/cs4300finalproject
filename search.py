import random
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
@dataclass
class pf_stats:
    total_depth: int = 0
    average_depth: float = 0
    total_wins: int = 0
    total_runs: int = 0
    win_rate: float = 0.0
    nodes_generated: int = 0
def default_dfs(problem: "Colony_Wrapper", attempts: int):
    frontier = [(Node(problem.initial_state), 0)]
    total_depth = 0
    last_seen_state: "None | Colony" = None
    while frontier:
        node, depth = frontier.pop()
        last_seen_state = node.state
        if problem.goal_test(node.state):
            return(True, node.state)
        chosen_action_list: list[Callable] = []
        action_stats: list[tuple[str, int]] = []
        available_energy = node.state.energy
        for i in range(problem.actions_per_day):
            action_list = problem.get_actions(node.state, available_energy)
            #If the actions stay static for the entire run I might be able to just compute them at the start rather than computing it in this inner loop
            if action_list:
                name, action, cost = random.choice(action_list)
                available_energy -= cost
                chosen_action_list.append(action)
                action_stats.append((name, cost))
            else:
                break
                #This might be entirely redundant because the loop only runs an amount equal to the actions per day
        newState = problem.transition(node.state, chosen_action_list)
        total_depth += 1
        if not newState.check_loss():
            frontier.append((Node(newState, tuple(action_stats), node), total_depth))
            
    return (False, last_seen_state)

def heuristic_dfs(problem: "Colony_Wrapper", attempts: int):
    pass    
#This function attempts to roughly determine how many realistic win conditions there are
def percentage_fuzzing(problem: "Colony_Wrapper", attempts: int=100000) -> "pf_stats": #bool return type is temporary just to make sure things run right
    stats = pf_stats()

    for i in range(attempts):
        frontier = [(Node(problem.initial_state), 0)]
        total_depth = 0
        stats.total_runs += 1
        while frontier:
            node, depth = frontier.pop()
            if problem.goal_test(node.state):
                stats.total_wins += 1
                break
            chosen_action_list: list[Callable] = []
            action_stats: list[tuple[str, int]] = []
            available_energy = node.state.energy
            for i in range(problem.actions_per_day):
                action_list = problem.get_actions(node.state, available_energy)
                if action_list:
                    name, action, cost = random.choice(action_list)
                    available_energy -= cost
                    chosen_action_list.append(action)
                    action_stats.append((name, cost))
                else:
                    break
                    #This might be entirely redundant because the loop only runs an amount equal to the actions per day
            newState = problem.transition(node.state, chosen_action_list)
            total_depth += 1
            if not newState.check_loss():
                frontier.append((Node(newState, tuple(action_stats), node), total_depth))
                stats.nodes_generated += 1
                stats.total_depth += 1
    stats.win_rate = stats.total_wins / stats.total_runs
    stats.average_depth = stats.total_depth / stats.total_runs
    return stats
            


        
    #Up next, set up the frontier and this search should be good to go