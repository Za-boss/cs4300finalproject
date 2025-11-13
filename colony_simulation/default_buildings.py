from typing import TYPE_CHECKING
from building import Building
if TYPE_CHECKING:
    from colony import Colony
def farm_tick_effect(colony : "Colony", efficiency: float):
    colony.food += round(15 * efficiency)

def nuclear_reactor_tick_effect(colony: "Colony", efficiency: float):
    colony.energy += round(20 * efficiency)

farm = Building("Farm", farm_tick_effect) 
nuclear_reactor = Building("Nuclear reactor", nuclear_reactor_tick_effect)
barracks = Building("Barracks", defense_strength=50)