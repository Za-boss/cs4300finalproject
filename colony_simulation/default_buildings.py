from colony_simulation.building import Building

farm = Building("Farm", production={"food": 15})
nuclear_reactor = Building("Nuclear reactor", production={"energy": 50})
space_port = Building("Space Port", production={"population": 3, "food": 2})
military_academy = Building("Military Academy", production={"defense": 3}, building_cost=100, staff_needed=20)
barracks = Building("Barracks", defense_strength=50 , production={"defense": 0})

ALL_BUILDINGS = [
    farm,
    nuclear_reactor,
    space_port,
    military_academy,
    barracks
]