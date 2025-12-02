#This class wraps a colony in a wrapper and makes it easier for the search algorithm to interact with
import math
from typing import Callable, TYPE_CHECKING
from colony_simulation.colony import Colony, get_colony_actions
from colony_simulation.building import Building, get_building_actions

if TYPE_CHECKING:
    from run import Heuristic_Values

class Colony_Wrapper:
    def __init__(
            self, 
            initial_state: Colony,
            available_buildings: list["Building"],
            heuristic_values: "Heuristic_Values"
        ) -> None:
        self.goal_day: int = 31
        self.initial_state: Colony = initial_state
        self.available_buildings: list["Building"] = available_buildings
        self.heuristic_values = heuristic_values
        self.actions_per_day: int = 3
        self.actions_taken: int = 0
    def get_actions(self, colony_state: Colony, available_energy: float) -> list[tuple[str, Callable, int]]:
        colony_actions = [
            action for action in get_colony_actions() 
            if available_energy >= action[2] or action[2] == 0
        ]
        building_actions = [
            action for action in get_building_actions(self.available_buildings) 
            if available_energy >= action[2] or action[2] == 0
        ]
        actions = colony_actions + building_actions
        return actions
    def transition(
            self, 
            colony_state: Colony, 
            action_list: list[tuple[str, Callable, int]]
        ) -> Colony:
        new_state: Colony = Colony(
            [b.clone() for b in colony_state.buildings], 
            colony_state.events[:], 
            food=colony_state.food,
            base_defense_capacity=colony_state.base_defense_capacity,
            population=colony_state.population,
            energy=colony_state.energy,
            base_food_production=colony_state.base_food_production,
            base_energy_production=colony_state.base_energy_production,
            population_growth_factor=colony_state.population_growth_factor
        )
        new_state.current_day = colony_state.current_day
        for _name, action, cost in action_list:
            action(new_state)
            new_state.energy -= cost

        new_state.calc_building_power_modifiers()

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

        def get_production_value(building: "Building", resource: str) -> int:
            return building.production.get(resource, 0)
        if colony_state.check_loss():
            return -1e6


        growth = colony_state.population * (colony_state.population_growth_factor + colony_state.temp_population_growth_factor)
        if growth >= 0:
            growth = max(2, math.ceil(growth))
        else:
            growth = min(-2, math.floor(growth))
        
        if colony_state.food <= 0:
            growth -= max(10, math.ceil(colony_state.population // 10))

        expected_pop = colony_state.population + growth


        total_staff_needed = sum(b.staff_needed for b in colony_state.buildings)
        
        if total_staff_needed > 0:
            projected_efficiency = min(1.0, expected_pop / total_staff_needed)
        else:
            projected_efficiency = 1.0


        building_food_prod = 0.0
        building_energy_prod = 0.0
        building_population_prod = 0.0
        building_defense_prod = 0.0
        building_extra_defense = 0.0

        if colony_state.buildings:
            for building in colony_state.buildings:
                building_food_prod += get_production_value(building, 'food') * projected_efficiency
                building_energy_prod += get_production_value(building, 'energy') * projected_efficiency
                building_population_prod += get_production_value(building, 'population') * projected_efficiency
                building_defense_prod += get_production_value(building, 'defense') * projected_efficiency
                if building.defense_strength:
                    building_extra_defense += building.defense_strength
                

        food_target = max(self.heuristic_values.food_target_base, colony_state.population * (colony_state.food_consumption_factor + 0.5))
        effective_food = colony_state.food + colony_state.base_food_production + building_food_prod
        food_score = effective_food / food_target

        energy_target = self.heuristic_values.energy_target
        effective_energy = colony_state.energy + colony_state.base_energy_production + building_energy_prod
        energy_score = effective_energy / energy_target

        defense_target = self.heuristic_values.defense_target
        effective_defense = colony_state.defense_capacity + building_defense_prod + building_extra_defense
        defense_score = effective_defense / defense_target

        population_target = self.heuristic_values.population_target
        effective_population = expected_pop + building_population_prod
        population_score =  effective_population / population_target

        # Weighted combination (weights chosen to reflect relative importance)
        w_food = self.heuristic_values.w_food
        w_energy = self.heuristic_values.w_energy
        w_defense = self.heuristic_values.w_defense
        w_population = self.heuristic_values.w_population

        if projected_efficiency < self.heuristic_values.efficiency_target:
            w_population = self.heuristic_values.below_efficiency_population_w
        if effective_food < food_target * .2: w_food = self.heuristic_values.below_food_target_food_w
        if effective_energy < 0: w_energy = self.heuristic_values.below_energy_target_energy_w

        total_weight = w_food + w_energy + w_defense + w_population

        combined = (
            w_food * food_score
            + w_energy * energy_score
            + w_defense * defense_score
            + w_population * population_score
        ) / total_weight

        return float(combined)