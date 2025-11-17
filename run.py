#!/usr/bin/env python3

import argparse
from search import *
from colony_simulation.colony import *
from colony_simulation.building import *
from colony_simulation.wrapper import Colony_Wrapper
from colony_simulation.default_buildings import *
from colony_simulation.default_events import *

def setup_simulation() -> tuple[Colony, list[Building]]:
    buildings = [nuclear_reactor.clone(), nuclear_reactor.clone()]
    available_buildings = [nuclear_reactor, farm, barracks]
    events = [meteor_strike, alien_invasion, alien_infection]
    colony_state = Colony(starting_buildings=buildings, events=events)
    colony_state.food_consumption_factor = 3
    colony_state.population = 100

    return (colony_state, available_buildings)

algorithms = {
    "default_dfs" : default_dfs,
    "heuristic_dfs" : heuristic_dfs,
    "percentage_fuzzing" : percentage_fuzzing
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Agent runner for running the colony management agent")
    parser.add_argument('--algorithm', '--algo', type=str, choices=algorithms.keys(), required=False, default="default_dfs", help="What algorithm to use for this run of the colony management agents")
    parser.add_argument('--run_count', "--rc", type=int, default=10, required=False)

    args = parser.parse_args()
    algorithm = algorithms[args.algorithm]
    run_count = args.run_count

    colony, buildings = setup_simulation()
    colony_wrapper = Colony_Wrapper(colony, buildings)
    colony_wrapper.goal_day = 31

    success, state = algorithm(colony_wrapper, run_count)
    if success and state:
        print(success)

        print(f"""Colony stats:
                Food: {state.food}
                Population: {state.population}
                defense readiness: {state.defense_capacity}
                Energy stockpiles: {state.energy}
                buildings: {state.buildings}""")
    else:
        print("whoops, you lost")
        print(f"""Colony stats:
                Food: {state.food}
                Population: {state.population}
                defense readiness: {state.defense_capacity}
                Energy stockpiles: {state.energy}
                buildings: {state.buildings}""")




    #Start by implementing a basic version of the "fuzzer" which is basic DFS first

if __name__ == "__main__":
    main()