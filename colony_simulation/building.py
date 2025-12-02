#Buildings should produce stuff like food and increase defense readiness
#Buildings are constructed using energy
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from colony import Colony

class Building:
    def __init__(
            self, 
            building_name: str,
            defense_strength: int = 0,
            staff_needed: int = 10,
            building_cost: int = 50,
            production: dict[str, int] = {},
        ):

        self.building_name: str = building_name
        self.defense_strength: int = defense_strength
        self.staff_needed = staff_needed
        self.building_cost: int = building_cost
        self.power_modifier: float = 1.0
        self.production: dict[str, int] = production
        self.valid_production_keys = ["food", "energy", "population", "defense"]

        #I might want to consider having the effects be tied to the building itself rather than a tick effect so that upgrades and stuff are easier to make
    def build(self, colony: "Colony") -> tuple[bool, str]:
        if colony.energy >= self.building_cost:
            colony.buildings.append(self.clone())
            return (True, f"Successfully built: {self.building_name}")
        else:
            return (False, f"Failed to build: {self.building_name}: lack of energy")
        
    def clone(self) -> "Building":
        return Building(
            self.building_name,
            self.defense_strength,
            self.staff_needed,
            self.building_cost,
            self.production
        )
        
    def tick_effect(self, colony: "Colony") -> None:
        if not self.production:
            return
        for resource, value in self.production.items():
            if resource not in self.valid_production_keys:
                continue
            adjusted_value = round(value * self.power_modifier)
            if resource == "food":
                colony.food += adjusted_value
            elif resource == "energy":
                colony.energy += adjusted_value
            elif resource == "population":
                colony.population += adjusted_value
            elif resource == "defense":
                colony.base_defense_capacity += adjusted_value
        
    def __repr__(self) -> str:
        return f"{self.building_name} efficiency: {self.power_modifier}"

def get_building_actions(buildings: list[Building]) -> list[tuple[str, Callable, int]]:
    building_actions = []
    for building in buildings:
        building_actions.append((
                f'Build: {building.building_name}',
                building.build,
                building.building_cost
            )
        )
    return building_actions

