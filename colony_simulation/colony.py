from typing import TYPE_CHECKING, Callable
import random
import math
if TYPE_CHECKING:
    from building import Building
    from colony_simulation.event import Event
# future additions that are optional:
# status effects: statuses that effect aspects about the colony over time
# lingering event effects, statuses that are applied when an event fires
# building upgrades - this one is probably going to be a very big optional one, may be implemented as an upgrade that just happens after a certain amount of days of existing
# buildings that only provide upgrades when they're

#mechanic addition ideas:
# -colony modifiers (chosen at start)
# -morale (a morale value that effects multiple aspects of the colony)
# -more effects from events and the like
# -flavor to buildings

class Colony:
    def __init__(
            self, 
            starting_buildings : list["Building"],
            events: list["Event"],
            food: float = 600, 
            base_defense_capacity: float = 70.0,
            population: int = 200,
            energy: float = 150.0,
            base_food_production: float = 30,
            base_energy_production: float = 50,
            population_growth_factor: float = 0.02,
        ):
        self.current_day: int = 1
        self.base_defense_capacity: float = base_defense_capacity
        self.food : float = food
        self.base_food_production: float = base_food_production
        self.population: int = population
        self.buildings: list["Building"] = starting_buildings
        self.energy: float = energy
        self.base_energy_production: float = base_energy_production
        self.events: list["Event"] = events
        self.current_effects: list[tuple[Callable, int]] = []
        self.population_growth_factor: float = population_growth_factor
        self.temp_population_growth_factor: float = 0.0
        self.temp_energy_production_modifier: float = 1.0
        self.food_consumption_factor: float = 2.0
        self.has_lost = False
        self.defense_capacity: float = self.calc_defense_capacity()
        #consider adding a population capacity somewhere

    def calc_building_power_modifiers(self) -> None:
        total_staff_needed = 0
        for building in self.buildings:
            total_staff_needed += building.staff_needed
        if total_staff_needed == 0:
            return # no buildings at all
        fulfillment_ratio = min(1, self.population / total_staff_needed)
        for building in self.buildings:
            building.power_modifier = max(0, fulfillment_ratio)
        #There may be a minor bug in here somewhere

    def calc_defense_capacity(self) -> float:
        if not self.buildings:
            return self.base_defense_capacity
        extra_defense = 0

        for building in self.buildings:
            if building.defense_strength == 0:
                continue
            extra_defense += building.defense_strength * building.power_modifier

        return self.base_defense_capacity + extra_defense
    
    def run_building_effects(self) -> None:
        if not self.buildings:
            return        
        for building in self.buildings:
            building.tick_effect(self)

    def run_events(self) -> None:
        for event in self.events:
            if not event.fire_dates:
                continue
            if self.current_day in event.fire_dates:
                event.fire_event(self)
    
    def apply_effects(self) -> None:
        continued_effects = []
        for effect, duration in self.current_effects:
            effect(self)

            duration -= 1

            if duration > 0:
                continued_effects.append((effect, duration))
            else:
                print(f'Effect {effect.__name__} has expired')

        self.current_effects = continued_effects

    def calc_population_change(self) -> None:
        
        population_change = self.population * (self.population_growth_factor + self.temp_population_growth_factor)
        if population_change >= 0:
            population_change = max(2, math.ceil(population_change))
        else:
            population_change = min(-2, math.floor(population_change))
        self.population += population_change
        
        if self.food <= 0:
            self.population -= max(10, math.ceil(self.population // 10)) # 10 people or 10% of the population, whichever is greater
        self.population = max(0, self.population) # prevents population from going negative 
        #if the population increase factor is greater then the decrease factor the population will grow and vice versa 
        #the population will decrease every tick, the decrease factor will change based on events and whether or not food is in surplus or deficit 

    def calc_food_consumption(self) -> None:
        self.food -= round(self.population / self.food_consumption_factor)
    def check_loss(self):
        if self.population <= 0:
            return True
        return False
    def tick_step(self) -> None:
        #Set to 0 so they can be modified
        self.temp_population_growth_factor = 0 
        self.temp_energy_production_modifier = 1.0

        self.food += self.base_food_production
        self.calc_food_consumption()
        self.calc_population_change()
        self.calc_building_power_modifiers()
        self.defense_capacity = self.calc_defense_capacity()
        self.run_building_effects()
        self.apply_effects()
        self.run_events()
        self.current_day += 1

        self.energy += self.base_energy_production * self.temp_energy_production_modifier

        self.population = max(0, self.population)


def get_colony_actions() -> list[tuple[str, Callable, int]]:
    food_investment_cost = 50
    def invest_in_food_production(colony: "Colony") -> tuple[bool, str]:
        colony.base_food_production *= 1.06
        return (True, "Food production successfully invested in")
    
    energy_investment_cost = 50
    def invest_in_energy_production(colony: "Colony") -> tuple[bool, str]:
        colony.base_energy_production *= 1.08
        return (True, "Energy production successfully invested in")
    
    defense_investment_cost = 50
    def invest_in_defense(colony: "Colony") -> tuple[bool, str]:
        colony.base_defense_capacity*=1.02
        return (True, "Defense successfully invested in")
    
    population_investment_cost = 50
    def invest_in_population_increase(colony: "Colony") -> tuple[bool, str]:
        colony.population_growth_factor *= 1.04
        return (True, "Population increase successfully invested in")
    
    staff_recruitment_cost = 50
    def recruit_staff(colony: "Colony") -> tuple[bool, str]:
        colony.population += 20
        return (True, "Successfully recruited 10 new staff members")
    
    do_nothing_cost = 0 # lol
    def do_nothing(colony: "Colony"):
        return (True, "Successfully did nothing")
    
    return [
        ("invest in food production", invest_in_food_production, food_investment_cost),
        ("invest in energy production", invest_in_energy_production, energy_investment_cost),
        ("invest in defense", invest_in_defense, defense_investment_cost),
        ("invest in population increase", invest_in_population_increase, population_investment_cost),
        ("recruit staff", recruit_staff, staff_recruitment_cost),
        ("Do nothing", do_nothing, do_nothing_cost)
    ]

