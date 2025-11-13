#Buildings should produce stuff like food and increase defense readiness
#Buildings are constructed using energy
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from colony import Colony

class Building:
    def __init__(
            self, 
            building_name: str,
            tick_effect: Callable | None = None,
            defense_strength: int = 0,
            staff_needed: int = 10,
            building_cost: int = 50,
        ):
        self.building_name: str = building_name
        self.defense_strength: int = defense_strength
        self.staff_needed = staff_needed
        self.building_cost: int = building_cost
        self.tick_effect: Callable | None = tick_effect

        #I might want to consider having the effects be tied to the building itself rather than a tick effect so that upgrades and stuff are easier to make
    def build(self, colony: "Colony") -> tuple[bool, str]:
        if colony.energy >= self.building_cost:
            colony.buildings.append(self.clone())
            colony.energy -= self.building_cost
            return (True, f"Successfully built: {self.building_name}")
        else:
            return (False, f"Failed to build: {self.building_name}: lack of energy")
    def clone(self) -> "Building":
        return Building(self.building_name, self.tick_effect, self.defense_strength, self.staff_needed, self.building_cost)


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