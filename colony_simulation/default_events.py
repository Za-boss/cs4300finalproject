from typing import TYPE_CHECKING
import random
from colony_simulation.event import *
if TYPE_CHECKING:
    from colony import Colony

# ===== POSITIVE EVENTS (Unchanged or slightly tweaked) =====

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
    colony.food += random.randint(150, 300)

def underground_discovery_event_fire(colony: "Colony") -> None:
    colony.base_energy_production += 5

def strange_signal_event_fire(colony: "Colony") -> None:
    # Neutral/Mixed
    if random.random() > 0.5:
        colony.energy += 50
    else:
        colony.energy -= 20

# ===== NEGATIVE EVENTS (BUFFED FOR HARD MODE) =====

def annihilate_colony_event_fire(colony: "Colony") -> None:
    # severe late game check: -100 population
    # If you haven't scaled population > 100 by now, this ends the run.
    colony.population -= 100

def cosmic_radiation_event_fire(colony: "Colony") -> None:
    """Radiation causes sickness"""
    loss = random.randint(15, 25) # Buffed from 5-10
    colony.population -= loss

def dust_storm_event_fire(colony: "Colony") -> None:
    """Reduces energy production and stores"""
    colony.energy -= 100 # Buffed from 30
    
    def storm_effect(colony: "Colony"):
        # Severe penalty: 40% efficiency (was 75%)
        colony.temp_energy_production_modifier = 0.40 
        
    colony.current_effects.append((storm_effect, 4)) # Lasts 4 days now

def alien_invasion_event_fire(colony: "Colony") -> None:
    """Aliens attack resources and population"""
    # Massive damage
    colony.population -= random.randint(30, 50)
    colony.food -= random.randint(200, 400)
    colony.energy -= random.randint(100, 200)
    # Permanent defense damage
    colony.base_defense_capacity *= 0.8

def alien_infection_event_fire(colony: "Colony") -> None:
    """Disease spreads"""
    colony.population -= random.randint(20, 40) # Buffed

def rocket_barrage_event(colony: "Colony") -> None:
    """Bombardment"""
    # Scales hard: Damage is 50 unless defense is extremely high
    damage = max(10, 50 - int(colony.defense_capacity * 0.1)) 
    colony.population -= damage
    colony.base_defense_capacity *= 0.9

def wildlife_encounter_event_fire(colony: "Colony") -> None:
    colony.food -= 50 # Buffed from 20

def escalating_raids_event_fire(colony: "Colony") -> None:
    # Multiplier increased from 3 to 15.
    # Day 10 = 150 Str. Day 20 = 300 Str. Day 30 = 450 Str.
    raid_strength = colony.current_day * 15 
    defense = colony.defense_capacity
    
    if defense < raid_strength:
        damage = raid_strength - defense
        # Heavy penalties for failing defense
        colony.population -= int(damage * 0.4) 
        colony.food -= int(damage * 2.0)
        colony.energy -= int(damage * 1.0)

def resource_depletion_event_fire(colony: "Colony") -> None:
    colony.base_food_production -= 5 # Buffed from 2

# ===== NEW HARD EVENTS =====

def solar_flare_event_fire(colony: "Colony") -> None:
    """Wipes out stored energy and harms electronics"""
    colony.energy = 0
    colony.base_energy_production -= 5

def sabotage_event_fire(colony: "Colony") -> None:
    """Internal sabotage destroys defenses"""
    colony.base_defense_capacity -= 50
    colony.food -= 100

def seismic_activity_event_fire(colony: "Colony") -> None:
    """Earthquake damages infrastructure"""
    # Removes a building effectively by reducing base stats permanently
    # representing a collapsed building
    colony.base_energy_production -= 10
    colony.base_food_production -= 10
    colony.population -= 15

# ===== MASSIVE RAIDS (From your list) =====

def massive_raid_one(colony: "Colony") -> None:
    raid_strength = 200
    defense = colony.defense_capacity
    if defense < raid_strength:
        damage = raid_strength - defense
        colony.population -= int(damage * 0.3) 
        colony.food -= int(damage * 2)
        colony.energy -= int(damage * 0.7)

def massive_raid_two(colony: "Colony") -> None:
    raid_strength = 400
    defense = colony.defense_capacity
    if defense < raid_strength:
        damage = raid_strength - defense
        colony.population -= int(damage * 0.7) 
        colony.food -= int(damage * 2)
        colony.energy -= int(damage * 0.7)

def massive_raid_three(colony: "Colony") -> None:
    raid_strength = 600
    defense = colony.defense_capacity
    if defense < raid_strength:
        damage = raid_strength - defense
        colony.population -= int(damage * 1.0) # Kills 1 person per 1 damage leaked
        colony.food -= int(damage * 2)
        colony.energy -= int(damage * 0.7)

# ===== EVENT SCHEDULE =====

# Early Game Support
supply_drop = Event(event_name="supply_drop", fire_event=supply_drop_event_fire, firing_likelihood=0.15, fire_count=3)
population_boom = Event(event_name="population_boom", fire_event=population_boom_event_fire, fire_dates=(8, 16))
discovery = Event(event_name="discovery", fire_event=discovery_event_fire, firing_likelihood=0.1, fire_count=2)
bountiful_harvest = Event(event_name="bountiful_harvest", fire_event=bountiful_harvest_event_fire, fire_dates=(5, 12))

# Mid Game Hazards
dust_storm = Event(event_name="dust_storm", fire_event=dust_storm_event_fire, firing_likelihood=0.12, fire_count=4)
alien_infection = Event(event_name="alien infection", fire_event=alien_infection_event_fire, fire_dates=(16, 24))
sabotage = Event(event_name="Sabotage", fire_event=sabotage_event_fire, fire_dates=(18, 26))

# Late Game Nightmares (The Gauntlet: Days 20-31)
massive_raid_one_event = Event(event_name="First massive raid (200)", fire_event=massive_raid_one, fire_dates=(13,))
massive_raid_two_event = Event(event_name="Second massive raid (400)", fire_event=massive_raid_two, fire_dates=(22,))
massive_raid_three_event = Event(event_name="Third massive raid (600)", fire_event=massive_raid_three, fire_dates=(29,))

alien_invasion = Event(event_name="Alien Invasion", fire_event=alien_invasion_event_fire, fire_dates=(25, 28, 30))
rocket_barrage = Event(event_name="Rocket Barrage", fire_event=rocket_barrage_event, fire_dates=(27, 31))
annihilate_colony = Event(event_name="Annihilation Attempt", fire_event=annihilate_colony_event_fire, fire_dates=(30,))
solar_flare = Event(event_name="Solar Flare", fire_event=solar_flare_event_fire, fire_dates=(23, 29))
seismic_activity = Event(event_name="Seismic Activity", fire_event=seismic_activity_event_fire, fire_dates=(20, 31))

# Persistent Threats
escalating_raids = Event(event_name="escalating_raids", fire_event=escalating_raids_event_fire, fire_dates=(21, 23, 24, 26, 28, 31))
resource_depletion = Event(event_name="resource_depletion", fire_event=resource_depletion_event_fire, fire_dates=(15, 20, 25, 30))

# Filler
strange_signal = Event(event_name="strange_signal", fire_event=strange_signal_event_fire, firing_likelihood=0.1, fire_count=2)
wildlife_encounter = Event(event_name="wildlife_encounter", fire_event=wildlife_encounter_event_fire, firing_likelihood=0.2, fire_count=8)
underground_discovery = Event(event_name="underground_discovery", fire_event=underground_discovery_event_fire, fire_dates=(10, 20))

ALL_EVENTS = [
    supply_drop,
    population_boom,
    discovery,
    bountiful_harvest,
    dust_storm,
    strange_signal,
    wildlife_encounter,
    underground_discovery,
    escalating_raids,
    resource_depletion,
    massive_raid_one_event,
    massive_raid_two_event,
    massive_raid_three_event,
    alien_invasion,
    alien_infection,
    rocket_barrage,
    annihilate_colony,
    solar_flare,
    sabotage,
    seismic_activity
]