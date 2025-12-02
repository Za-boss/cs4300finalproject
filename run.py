#!/usr/bin/env python3

import argparse
from search import *
from colony_simulation.colony import *
from colony_simulation.building import *
from colony_simulation.wrapper import Colony_Wrapper
from colony_simulation.default_buildings import *
from colony_simulation.default_events import *
import random
#Events should be encoded as: Event, Fire_date, Firing likelihood


# goes through a list of events, if the event has firing date(s), 
# if the event has a firing likelihood, generate a random number and add the event at the current day if the random number deems it so
def setup_events(events : list[Event], days : int):
    event_list = []
    event_removal_list = []
    for event in events:
        if event.fire_dates:
            event_list.append(event)
            event_removal_list.append(event)
        if event.firing_likelihood:
            fire_dates = []
            for i in range(1, days + 1):
                if random.random() <= event.firing_likelihood:
                    fire_dates.append(i)
                    event.fire_count -= 1
                    if event.fire_count <= 0:
                        event_removal_list.append(event)
                        break
            event.firing_likelihood = None
            event.fire_dates = tuple(fire_dates)
            event_list.append(event)
    for event in event_removal_list:
        events.remove(event)
    return event_list



def setup_simulation(expected_days : int) -> tuple[Colony, list[Building]]:
    buildings = [farm.clone(), nuclear_reactor.clone()]
    available_buildings = [building for building in ALL_BUILDINGS]
    events = [event for event in ALL_EVENTS]
    event_list = setup_events(events, expected_days)
    colony_state = Colony(starting_buildings=buildings, events=event_list)

    colony_state.food_consumption_factor = 2
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
    parser.add_argument('--attempt_count', "--ac", type=int, default=100, required=False)
    parser.add_argument('--seed', '--s', type=int, required=False)
    parser.add_argument('--display_timeline', '--dt', type=bool, required=False, default=False)
    args = parser.parse_args()
    seed = args.seed
    if not seed:
        seed = random.randrange(10000000)
    random.seed(seed)
    print(f"Seed for this run: {seed}")
    algorithm = algorithms[args.algorithm]
    run_count = args.run_count
    attempt_count = args.attempt_count
    display_timeline = args.display_timeline
    GOAL_DAYS = 31
    colony, buildings = setup_simulation(GOAL_DAYS)
    colony_wrapper = Colony_Wrapper(colony, buildings)
    colony_wrapper.goal_day = GOAL_DAYS
    if args.algorithm == "percentage_fuzzing":
        stats = algorithm(colony_wrapper, run_count)
        print(f"""Percentage fuzzing stats:
                Win rate: {stats.win_rate}
                Total wins: {stats.total_wins}
                Total runs: {stats.total_runs}
                Total depth: {stats.total_depth}
                Average depth: {stats.average_depth}
                Nodes generated: {stats.nodes_generated}""")
        return
    path, stats = algorithm(colony_wrapper, attempt_count)
    print(f"""Search stats:
                Attempts needed: {stats.attempts_needed}
                Nodes generated: {stats.nodes_generated}
                Nodes explored: {stats.nodes_explored}
                Average depth: {stats.average_depth}
                Success: {stats.success}""")
    if not display_timeline or not path:
        return
    
    print("Colony timeline:")
    for day, node in enumerate(path):
        print(day)
        print(f"Actions: {node.actions}")
        print(f"Energy: {node.state.energy}")
        print(f"Population: {node.state.population}")
        print(f"Defense: {node.state.defense_capacity}")
        print(f"Food: {node.state.food}")
        print(f"Total buildings: {len(node.state.buildings)}")

        print("Events:")
        for event in colony.events:
            if not event.fire_dates:
                continue
            if day in event.fire_dates:
                print(event.event_name)

    #Start by implementing a basic version of the "fuzzer" which is basic DFS first

if __name__ == "__main__":
    main()