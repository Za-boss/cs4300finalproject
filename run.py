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

    return (colony_state, available_buildings)

algorithms = {
    "default_dfs" : default_dfs,
    "heuristic_dfs" : heuristic_dfs,
    "percentage_fuzzing" : percentage_fuzzing
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Agent runner for running the colony management agent")
    parser.add_argument('--algorithm', '--algo', type=str, choices=algorithms.keys(), required=True, help="What algorithm to use for this run of the colony management agents")
    parser.add_argument('--run_count', "--rc", type=int, default=10, required=False)

    args = parser.parse_args()
    algorithm = algorithms[args.algo]
    run_count = args.rc

    colony, buildings = setup_simulation()
    colony_wrapper = Colony_Wrapper(colony, buildings)

    success = algorithm(colony_wrapper, run_count)

    print(success)




    #Start by implementing a basic version of the "fuzzer" which is basic DFS first

if __name__ == "__main__":
    main()