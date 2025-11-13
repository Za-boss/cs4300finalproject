#This class wraps a colony in a wrapper and makes it easier for the search algorithm to interact with
from typing import TYPE_CHECKING, Callable
from colony import Colony, get_colony_actions
from building import Building, get_building_actions

#Remove these imports once you move the simulation setup out of this file
from default_buildings import *
from default_events import *

if TYPE_CHECKING:
    from colony import Colony
    from building import Building
class Colony_Wrapper:
    def __init__(
            self, 
            initial_state: Colony,
            available_buildings: list["Building"]
        ) -> None:
        self.current_day: int = 0 
        self.initial_state: Colony = initial_state
        self.available_buildings: list["Building"] = available_buildings
        self.actions_per_day: int = 3
        self.actions_taken: int = 0
    def get_actions(self, colony_state: Colony) -> list[tuple[str, Callable, int]] | None:
        if self.actions_taken >= self.actions_per_day:
            self.actions_taken = 0
            # colony_state.tick_step() remember to call the tick step sometime
            return None
        colony_actions = [
            action for action in get_colony_actions() 
            if colony_state.energy >= action[2] or action[2] == 0 and not action[2] < 0
        ]
        building_actions = [
            action for action in get_building_actions(self.available_buildings) 
            if colony_state.energy >= action[2] or action[2] == 0 and not action[2] < 0
        ]
        actions = colony_actions + building_actions
        return actions
    def transition(
            self, 
            colony_state: Colony, 
            action: tuple[str, Callable, int] | None
        ) -> Colony:
        new_state: Colony = Colony(colony_state.buildings[:], colony_state.events[:])
        #I may want to just quietly advance the day and not generate a whole new state for the new day
        if action is None:
            new_state.current_day += 1
            return new_state
        action_func = action[1]
        action_func(new_state)
        return new_state
    def goal_test(self, colony_state: Colony) -> bool:
        return (colony_state.current_day >= self.current_day)
    def step_cost(self) -> float:
        return 1.0
    def heuristic(self) -> None:
        pass