import random
from typing import TYPE_CHECKING, Any, Optional
from dataclasses import dataclass
if TYPE_CHECKING:
    from colony_simulation.wrapper import Colony_Wrapper
    from colony_simulation.colony import Colony

#This node class will need to change, it's just a template as of now
#May also need to include some sort of stats dataclass that stores the stats of the agent
@dataclass
class Node:
    state: "Colony"
    action: Optional[tuple[str, int]] = None
    parent: Optional["Node"] = None

def default_dfs(problem: "Colony_Wrapper", attempts: int):
    frontier = [(Node(problem.initial_state), 0)]
    total_depth = 0
    last_seen_state: "None | Colony" = None
    while frontier:
        node, depth = frontier.pop()
        last_seen_state = node.state
        if problem.goal_test(node.state):
            return (True, node.state)
        
        action_list = problem.get_actions(node.state)
        if action_list:
            name, action, cost = random.choice(action_list)
        else:
            action = None
        newState = problem.transition(node.state, action)
        total_depth += 1
        if not newState.check_loss():
            frontier.append((Node(newState), total_depth))
    
    return (False, last_seen_state)

def heuristic_dfs(problem: "Colony_Wrapper", attempts: int):
    pass
#This function attempts to roughly determine how many realistic win conditions there are
def percentage_fuzzing(problem: "Colony_Wrapper", attempts: int=100000) -> None: #bool return type is temporary just to make sure things run right
    pass

        
    #Up next, set up the frontier and this search should be good to go