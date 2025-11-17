from typing import TYPE_CHECKING
import random
from colony_simulation.events import *
if TYPE_CHECKING:
    from colony import Colony
def building_destroy_event_fire(colony: "Colony") -> None:
    print("Meteor strike has occurred")
    if colony.buildings:
        building = random.choice(colony.buildings)
        colony.buildings.remove(building)
    else:
        colony.population -= 10

def alien_invasion_event_fire(colony: "Colony") -> None:
    print("alien invasion has occurred")
    if colony.defense_capacity >= 75:
        colony.population -= 15
    else:
        colony.population -= 25

def alien_infection_event_fire(colony: "Colony") -> None:
    def infection_effect(colony: "Colony"):
        colony.temp_population_decrease_factor += 0.1 #This can be used as a template for effect functions that apply continuous effects, this inner function will fire on every tick until its duration is up
    
    colony.current_effects.append((infection_effect, 3))
    print ("alien infection has occurred")
    colony.population -= 10


meteor_strike_test = {
    "event_name": "meteor_strike",
    "fire_event": building_destroy_event_fire,
    "fire_dates": (3, 7, 19),
}
alien_invasion_test = {
    "event_name": "alien_invasion",
    "fire_event": building_destroy_event_fire,
    "firing_likelihood": 0.2,
    "fire_count": 3
}
alien_infection_test = {
    "event_name": "meteor_strike",
    "fire_event": building_destroy_event_fire,
    "fire_dates": (5, 20),
}

meteor_strike = Event(event_name="meteor_strike", fire_event=building_destroy_event_fire, fire_dates=(3, 7, 19))

alien_invasion = Event(event_name="alien_invasion", fire_event=alien_invasion_event_fire, firing_likelihood=.2, fire_count=3)

alien_infection = Event(event_name="alien infection", fire_event=alien_infection_event_fire, fire_dates=(5, 20, 31))

#An interesting idea might be having events that only fire when certain thresholds have been met, ie some buildings existing or not or some values being met