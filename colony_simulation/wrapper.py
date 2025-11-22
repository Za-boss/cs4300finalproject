#This class wraps a colony in a wrapper and makes it easier for the search algorithm to interact with
from typing import Callable
from colony_simulation.colony import Colony, get_colony_actions
from colony_simulation.building import Building, get_building_actions

class Colony_Wrapper:
    def __init__(
            self, 
            initial_state: Colony,
            available_buildings: list["Building"]
        ) -> None:
        self.goal_day: int = 31
        self.initial_state: Colony = initial_state
        self.available_buildings: list["Building"] = available_buildings
        self.actions_per_day: int = 3
        self.actions_taken: int = 0
    def get_actions(self, colony_state: Colony, available_energy: float) -> list[tuple[str, Callable, int]] | None:
        if self.actions_taken >= self.actions_per_day:
            self.actions_taken = 0
            # colony_state.tick_step() remember to call the tick step sometime
            return None
        colony_actions = [
            action for action in get_colony_actions() 
            if available_energy >= action[2] or action[2] == 0 and not action[2] < 0
        ]
        building_actions = [
            action for action in get_building_actions(self.available_buildings) 
            if available_energy >= action[2] or action[2] == 0 and not action[2] < 0
        ]
        actions = colony_actions + building_actions
        return actions
    def transition(
            self, 
            colony_state: Colony, 
            action_list: list[Callable]
        ) -> Colony:
        new_state: Colony = Colony(
            colony_state.buildings[:], 
            colony_state.events[:], 
            food=colony_state.food,
            base_defense_capacity=colony_state.base_defense_capacity,
            population=colony_state.population,
            energy=colony_state.energy
        )
        new_state.current_day = colony_state.current_day
        #I may want to just quietly advance the day and not generate a whole new state for the new day
        for action in action_list:
            action(new_state)
        new_state.tick_step()
        return new_state
    def goal_test(self, colony_state: Colony) -> bool:
        return (colony_state.current_day > self.goal_day)
    def fail_test(self, colony_state: Colony) -> bool:
        return colony_state.check_loss()
    def step_cost(self) -> float:
        return 1.0
    def heuristic(self) -> None:
        pass