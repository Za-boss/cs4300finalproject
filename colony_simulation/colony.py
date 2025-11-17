from typing import TYPE_CHECKING, Callable
import random
import math
if TYPE_CHECKING:
    from building import Building
    from events import Event
# future additions that are optional:
# status effects: statuses that effect aspects about the colony over time
# lingering event effects, statuses that are applied when an event fires
# building upgrades - this one is probably going to be a very big optional one, may be implemented as an upgrade that just happens after a certain amount of days of existing
# buildings that only provide upgrades when they're
class Colony:
    def __init__(
            self, 
            starting_buildings : list["Building"],
            events: list["Event"],
            food: int = 500, 
            base_defense_capacity: float = 50.0,
            population: int = 50,
            energy: int = 50
        ):
        self.current_day: int = 1
        self.base_defense_capacity: float = base_defense_capacity
        self.food : int = food
        self.base_food_production: int = 10
        self.population: int = population
        self.buildings: list["Building"] = starting_buildings
        self.energy: int = energy
        self.base_energy_production: int = 10
        self.events: list["Event"] = events
        self.current_effects: list[tuple[Callable, int]] = []
        self.base_population_decrease_factor: float = 0.02
        self.temp_population_decrease_factor: float = 0.0
        self.base_population_increase_factor: float = 0.04
        self.temp_population_increase_factor: float = 0.0
        self.food_consumption_factor: float = 2.0 
        self.has_lost = False
        self.defense_capacity: float = self.calc_defense_capacity()
        #consider adding a population capacity somewhere

    def calc_defense_capacity(self) -> float:
        if not self.buildings:
            return self.base_defense_capacity
        extra_defense = 0
        staff_per_building = self.population / len(self.buildings)

        for building in self.buildings:
            if building.defense_strength == 0:
                continue
            building.power_modifier = min(1, staff_per_building/building.staff_needed)
            extra_defense += building.defense_strength * building.power_modifier

        return self.base_defense_capacity + extra_defense
    
    def run_building_effects(self) -> None:
        if not self.buildings:
            return
        staff_per_building = self.population / len(self.buildings)
        
        for building in self.buildings:
            if building.tick_effect == None:
                continue
            building.power_modifier = min(1, staff_per_building / building.staff_needed)
            building.tick_effect(self, building.power_modifier)

    def run_events(self) -> None:
        for event in self.events:
            if not event.fire_dates:
                continue
            if self.current_day in event.fire_dates:
                print("event should fire")
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
        pre_calc_population = self.population
        
        population_added = max(2, math.ceil(self.population * (self.base_population_increase_factor + self.temp_population_increase_factor)))
        self.population += population_added
        
        population_decrease = math.ceil(pre_calc_population * (self.base_population_decrease_factor + self.temp_population_decrease_factor))
        self.population -=  population_decrease
        
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
        self.current_day += 1
        self.food += self.base_food_production
        self.energy += self.base_energy_production
        self.apply_effects()
        self.run_events()
        self.run_building_effects()
        self.defense_capacity = self.calc_defense_capacity()
        self.calc_food_consumption()
        self.calc_population_change()
        self.temp_population_decrease_factor = 0
        self.temp_population_increase_factor = 0 # setting these to 0 so they can be modified by temporary effects
        # if self.energy <= 0:
        #     self.has_lost = True

def get_colony_actions() -> list[tuple[str, Callable, int]]:
    #These invest actions should have some sort of cost but I'm not sure what it should be
    food_investment_cost = 10
    def invest_in_food_production(colony: "Colony") -> tuple[bool, str]:
        colony.energy -= food_investment_cost
        colony.base_food_production += 3
        return (True, "Food production successfully invested in")
    
    energy_investment_cost = 25
    def invest_in_energy_production(colony: "Colony") -> tuple[bool, str]:
        colony.energy -= energy_investment_cost
        colony.base_energy_production += 5
        return (True, "Energy production successfully invested in")
    
    defense_investment_cost = 10
    def invest_in_defense(colony: "Colony") -> tuple[bool, str]:
        colony.energy -= defense_investment_cost
        colony.base_defense_capacity += 10
        return (True, "Defense successfully invested in")
    
    population_investment_cost = 10
    def invest_in_population_increase(colony: "Colony") -> tuple[bool, str]:
        colony.energy -= population_investment_cost
        colony.base_population_increase_factor += 0.005
        return (True, "Population increase successfully invested in")
    
    do_nothing_cost = 0 # lol
    def do_nothing(colony: "Colony"):
        return (True, "Successfully did nothing")
    
    return [
        ("invest in food production", invest_in_food_production, food_investment_cost),
        ("invest in energy production", invest_in_energy_production, energy_investment_cost),
        ("invest in defense", invest_in_defense, defense_investment_cost),
        ("invest in population increase", invest_in_population_increase, population_investment_cost),
        ("Do nothing", do_nothing, do_nothing_cost)
    ]

