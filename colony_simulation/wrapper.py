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
        for action in action_list:
            action(new_state)
        return new_state
    def run_tick(self, state : Colony):
        state.tick_step()
    def goal_test(self, colony_state: Colony) -> bool:
        return (colony_state.current_day > self.goal_day)
    def fail_test(self, colony_state: Colony) -> bool:
        return colony_state.check_loss()
    def step_cost(self) -> float:
        return 1.0
    def heuristic(self, colony_state: Colony) -> float:
        """Evaluate a colony state and return a heuristic score (higher is better).

        The heuristic combines normalized metrics for food, energy, defense, and
        population into a single float in the range [0.0, 1.0]. If the colony has
        already lost, a strongly negative value is returned.
        """
        def get_production_value(building: "Building", resource: str) -> int:
            if resource in building.production.keys():
                return building.production[resource]
            return 0
        if colony_state.check_loss():
            return -1e6

        # Estimate building contributions taking staffing into account
        building_food_prod = 0.0
        building_energy_prod = 0.0
        building_population_prod = 0.0
        building_defense_prod = 0.0
        if colony_state.buildings:
            for building in colony_state.buildings:
                #Need to change this so it uses the production dictionary in the building
                power_modifier = building.power_modifier
                building_food_prod += get_production_value(building, 'food') * power_modifier
                building_energy_prod += get_production_value(building, 'energy') * power_modifier
                building_population_prod += get_production_value(building, 'population') * power_modifier
                building_defense_prod += get_production_value(building, 'defense') * power_modifier

        # normalized sub-scores in 0..1 (higher is better)
        # consider current stock + one-tick expected production
        food_target = max(1.0, colony_state.population * 4)
        effective_food = colony_state.food + colony_state.base_food_production + building_food_prod
        food_score = min(1.0, effective_food / food_target)

        energy_target = 150.0
        effective_energy = colony_state.energy + colony_state.base_energy_production + building_energy_prod
        energy_score = min(1.0, effective_energy / energy_target)

        defense_target = 150
        effective_defense = colony_state.defense_capacity + building_defense_prod
        defense_score = min(1.0, effective_defense / defense_target)

        population_target = 200
        effective_population = colony_state.population + building_population_prod
        population_score = min(1.0, effective_population / population_target)

        # Weighted combination (weights chosen to reflect relative importance)
        w_food = 3.0
        w_energy = 2.0
        w_defense = 2.0
        w_population = 3.0
        total_weight = w_food + w_energy + w_defense + w_population

        combined = (
            w_food * food_score
            + w_energy * energy_score
            + w_defense * defense_score
            + w_population * population_score
        ) / total_weight

        return float(combined)