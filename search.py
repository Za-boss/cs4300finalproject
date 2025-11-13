from typing import TYPE_CHECKING, Any, Optional
from dataclasses import dataclass
if TYPE_CHECKING:
    from colony_simulation.wrapper import Colony_Wrapper
    from colony_simulation.colony import Colony

#This node class will need to change, it's just a template as of now
#May also need to include some sort of stats dataclass that stores the stats of the agent
@dataclass
class Node:
    state: "Colony_Wrapper"
    action: Optional[Any] = None
    parent: Optional[Any] = None

def default_dfs(domain: "Colony_Wrapper", attempts: int):
    pass
def heuristic_dfs(domain: "Colony_Wrapper", attempts: int):
    pass
#This function attempts to roughly determine how many realistic win conditions there are
def percentage_fuzzing(domain: "Colony_Wrapper", attempts: int=100000):
    #Up next, set up the frontier and this search should be good to go
    return False