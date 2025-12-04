from colony_simulation.building import Building

farm = Building("Farm", production={"food": 45})
irrigator = Building("Irrigator", production={"food": 80}, building_cost=200, staff_needed=25)
nuclear_reactor = Building("Nuclear reactor", production={"energy": 50})
dyson_sphere = Building("Dyson Sphere", production={"energy": 200}, building_cost=500, staff_needed=50)
space_port = Building("Space Port", production={"population": 5, "food": 10})
metropolitan_hub = Building("Metropolitan Hub", production={"population": 20, "energy": 15}, building_cost=300, staff_needed=30)
military_academy = Building("Military Academy", production={"defense": 10}, building_cost=175, staff_needed=20)
barracks = Building("Barracks", defense_strength=65 , production={"defense": 0})

ALL_BUILDINGS = [
    farm,
    irrigator,
    nuclear_reactor,
    dyson_sphere,
    space_port,
    metropolitan_hub,
    military_academy,
    barracks
]