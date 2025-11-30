from colony_simulation.building import Building

farm = Building("Farm", production={"food": 15})
nuclear_reactor = Building("Nuclear reactor", production={"energy": 100})
space_port = Building("Space Port", production={"population": 5, "food": 3})
military_academy = Building("Military Academy", production={"defense": 5}, building_cost=100, staff_needed=20)
barracks = Building("Barracks", defense_strength=50)