from typing import TYPE_CHECKING
import random
from colony_simulation.event import *
if TYPE_CHECKING:
    from colony import Colony
def annihilate_colony_event_fire(colony: "Colony") -> None:
    colony.population -= 10000

from typing import TYPE_CHECKING
import random
from colony_simulation.event import *
if TYPE_CHECKING:
    from colony import Colony

#Some of the events in this file should be modified as it may be too harsh

# ===== POSITIVE EVENTS =====

def supply_drop_event_fire(colony: "Colony") -> None:
    """A supply ship arrives with resources"""
    colony.food += random.randint(100, 200)
    colony.energy += random.randint(30, 60)

def population_boom_event_fire(colony: "Colony") -> None:
    """Refugees or immigrants arrive"""
    new_population = random.randint(15, 30)
    colony.population += new_population

def discovery_event_fire(colony: "Colony") -> None:
    """Scientists make a breakthrough"""
    def research_boost(colony: "Colony"):
        colony.temp_population_growth_factor += 0.02
    
    colony.current_effects.append((research_boost, 5))
    colony.energy += 50

def bountiful_harvest_event_fire(colony: "Colony") -> None:
    """Crops yield exceptionally well"""
    colony.food += random.randint(150, 250)
    colony.base_food_production += 2

# ===== NEGATIVE EVENTS =====

def rocket_barrage_event(colony: "Colony") -> None:
    def barrage_effect(colony: "Colony"):
        buildings_to_remove = []
        chosen_indices = {}
        for i in range(2):
            if not colony.buildings:
                break
            building_destroyed = random.choice(colony.buildings)
            chosen_index = colony.buildings.index(building_destroyed)
            chosen_indices[chosen_index] = True
            while chosen_index in chosen_indices.keys():
                building_destroyed = random.choice(colony.buildings)
                chosen_index = colony.buildings.index(building_destroyed)
                chosen_indices[chosen_index] = True
            buildings_to_remove.append(random.choice(colony.buildings))
        if buildings_to_remove:
            for building in buildings_to_remove:
                colony.buildings.remove(building)
        colony.population -= 10

def building_destroy_event_fire(colony: "Colony") -> None:
    buildings_destroyed = 0
    for _ in range(2):
        if colony.buildings:
            building = random.choice(colony.buildings)
            colony.buildings.remove(building)
            buildings_destroyed += 1
    
    if buildings_destroyed == 0:
        colony.population -= 30

def alien_invasion_event_fire(colony: "Colony") -> None:
    if colony.defense_capacity >= 200:
        colony.population -= 20
    else:
        colony.population -= 40

def alien_infection_event_fire(colony: "Colony") -> None:
    def infection_effect(colony: "Colony"):
        colony.temp_population_growth_factor -= 0.15
    
    colony.current_effects.append((infection_effect, 5))
    colony.population -= 20

def solar_flare_event_fire(colony: "Colony") -> None:
    energy_loss = min(colony.energy * 0.60, colony.energy - 20)
    colony.energy -= energy_loss
    colony.base_energy_production = max(5, colony.base_energy_production - 5)

def plague_event_fire(colony: "Colony") -> None:
    def plague_effect(colony: "Colony"):
        colony.temp_population_growth_factor -= 0.25
        colony.population -= random.randint(5, 20)
    
    colony.current_effects.append((plague_effect, 10))
    colony.population -= random.randint(20, 40)

def food_contamination_event_fire(colony: "Colony") -> None:
    food_loss = int(min(colony.food * 0.75, colony.food - 100))
    colony.food -= food_loss
    colony.population -= random.randint(15, 25)

def dust_storm_event_fire(colony: "Colony") -> None:
    def storm_effect(colony: "Colony"):
        colony.base_food_production = max(5, colony.base_food_production - 5)
        colony.base_energy_production = max(5, colony.base_energy_production - 5)
    
    colony.current_effects.append((storm_effect, 6))

def equipment_failure_event_fire(colony: "Colony") -> None:
    colony.energy -= min(colony.energy * 0.50, colony.energy - 40)
    colony.base_defense_capacity = max(30, colony.base_defense_capacity - 30)

def strange_signal_event_fire(colony: "Colony") -> None:
    if random.random() < 0.5:
        colony.energy += 100
        colony.base_energy_production += 3
    else:
        colony.population -= random.randint(20, 30)
        colony.energy -= 100

def wildlife_encounter_event_fire(colony: "Colony") -> None:
    if colony.defense_capacity >= 150:
        colony.food += random.randint(50, 100)
    else:
        colony.population -= random.randint(15, 30)
        colony.food -= random.randint(50, 100)

def underground_discovery_event_fire(colony: "Colony") -> None:
    discovery_type = random.choice(['water', 'minerals', 'danger'])
    
    if discovery_type == 'water':
        colony.base_food_production += 5
    elif discovery_type == 'minerals':
        colony.energy += 150
        colony.base_energy_production += 4
    else:
        colony.population -= random.randint(15, 25)
        for _ in range(2):
            if colony.buildings:
                colony.buildings.remove(random.choice(colony.buildings))

def escalating_raids_event_fire(colony: "Colony") -> None:
    raid_strength = 100 + (colony.current_day * 4.0)
    
    if colony.defense_capacity >= raid_strength:
        colony.population -= random.randint(5, 10)
    else:
        colony.population -= random.randint(30, 50)
        colony.food -= random.randint(100, 200)
        colony.energy -= random.randint(60, 120)

def resource_depletion_event_fire(colony: "Colony") -> None:
    depletion_factor = min(0.75, colony.current_day * 0.015)
    colony.base_food_production = max(3, int(colony.base_food_production * (1 - depletion_factor)))
    colony.base_energy_production = max(3, int(colony.base_energy_production * (1 - depletion_factor)))

# Positive events
supply_drop = Event(event_name="supply_drop", fire_event=supply_drop_event_fire, firing_likelihood=0.15, fire_count=4)
population_boom = Event(event_name="population_boom", fire_event=population_boom_event_fire, fire_dates=(10, 12, 24))
discovery = Event(event_name="discovery", fire_event=discovery_event_fire, firing_likelihood=0.1, fire_count=2)
bountiful_harvest = Event(event_name="bountiful_harvest", fire_event=bountiful_harvest_event_fire, fire_dates=(15, 25))

# Negative events
solar_flare = Event(event_name="solar_flare", fire_event=solar_flare_event_fire, firing_likelihood=0.08, fire_count=3)
plague = Event(event_name="plague", fire_event=plague_event_fire, fire_dates=(15, 26))
food_contamination = Event(event_name="food_contamination", fire_event=food_contamination_event_fire, firing_likelihood=0.08, fire_count=3)
dust_storm = Event(event_name="dust_storm", fire_event=dust_storm_event_fire, firing_likelihood=0.12, fire_count=4)
equipment_failure = Event(event_name="equipment_failure", fire_event=equipment_failure_event_fire, fire_dates=(10, 22))
meteor_strike = Event(event_name="meteor_strike", fire_event=building_destroy_event_fire, fire_dates=(7, 20))
alien_invasion = Event(event_name="alien_invasion", fire_event=alien_invasion_event_fire, firing_likelihood=0.05, fire_count=2)
alien_infection = Event(event_name="alien infection", fire_event=alien_infection_event_fire, fire_dates=(14, 28))
rocket_barrage = Event(event_name="Rocket barrage", fire_event=rocket_barrage_event, firing_likelihood=0.05, fire_count=2)
# Neutral/choice events
strange_signal = Event(event_name="strange_signal", fire_event=strange_signal_event_fire, firing_likelihood=0.1, fire_count=2)
wildlife_encounter = Event(event_name="wildlife_encounter", fire_event=wildlife_encounter_event_fire, firing_likelihood=0.15, fire_count=8)
underground_discovery = Event(event_name="underground_discovery", fire_event=underground_discovery_event_fire, fire_dates=(9, 23, 28))

# Scaling events
escalating_raids = Event(event_name="escalating_raids", fire_event=escalating_raids_event_fire, firing_likelihood=0.18, fire_count=6)
resource_depletion = Event(event_name="resource_depletion", fire_event=resource_depletion_event_fire, fire_dates=(12, 24))

# Complete event list for easy import
ALL_EVENTS = [
    supply_drop,
    population_boom,
    discovery,
    bountiful_harvest,
    solar_flare,
    plague,
    food_contamination,
    dust_storm,
    equipment_failure,
    strange_signal,
    wildlife_encounter,
    underground_discovery,
    escalating_raids,
    resource_depletion,
    meteor_strike,
    alien_invasion,
    alien_infection,
    rocket_barrage
]



