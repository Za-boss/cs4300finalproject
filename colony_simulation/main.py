#!/usr/bin/env python3
# a main file for just testing the simulation itself

# When you come back to this consider doing the following:
# start hooking up the agent to a rudimentary version of the application
# build out the full 31 day simulation
# consider adding events that are added at random
# tweak around a few things to make sure it's funner to mess with
from colony import *
from default_buildings import *
from default_events import *
import sys

#This main file will not be functioning for the time being

def get_actions(colony : Colony, available_buildings: list[Building]) -> list[tuple[str, Callable, int]]:
    colony_actions = get_colony_actions()
    building_actions = [(f'Build: {building.building_name}', lambda b=building: b.build(colony)) for building in available_buildings]
    actions = colony_actions + building_actions
    return actions

def prepare_events():
    pass

def setup_simulation() -> tuple[Colony, list[Building]]:
    buildings = [nuclear_reactor.clone(), nuclear_reactor.clone()]
    available_buildings = [nuclear_reactor, farm, barracks]
    events = [meteor_strike, alien_invasion, alien_infection]
    colony_state = Colony(starting_buildings=buildings, events=events)

    return (colony_state, available_buildings)

def main() -> None:
    colony_state, available_buildings = setup_simulation()
    TOTAL_DAYS = 31
    loop_counts = 0

    while colony_state.current_day < TOTAL_DAYS and colony_state.has_lost != True:
        print(f"\n--- Day {colony_state.current_day} ---")
        print(f"Resources: Food: {colony_state.food}, Energy: {colony_state.energy}, Population: {colony_state.population}")
        print(f"Defense Readiness: {colony_state.defense_capacity}\n")
        for building in colony_state.buildings:
            print(f"Building: {building.building_name} | Staff needed: {building.staff_needed}")

        actions = get_actions(colony_state, available_buildings) # for this file, we should just get the actions, present them to the user, and execute whatever the user tells us to

        print("Available actions:")
        for i, (name, _) in enumerate(actions, start=1):
            print(f"  {i}. {name}\n")
        total_commands_allowed = 3
        total_commands_executed = 0
        while True:
            user_input = input("Choose an action by number (or type 'q' to quit): ").strip()
            if user_input.lower() == "q":
                sys.exit(0)
            if user_input == "":
                print("Day ending manually")
                break
            if not user_input.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            index = int(user_input) - 1
            if 0 <= index < len(actions):
                _, action_func = actions[index]
                # Execute the selected action
                result, msg = action_func()
                if result == True:
                    total_commands_executed += 1
                    print(msg)
                else:
                    print(msg)
                print(f"{total_commands_executed} command(s) have been executed, {total_commands_allowed - total_commands_executed} more allowed")
                
            else:
                print("Invalid choice. Please select a valid action number.")
            if total_commands_executed >= total_commands_allowed:
                print("Command cap reached, ending the day")
                break
        colony_state.tick_step()
        loop_counts += 1
        print(f'Total loop counts: {loop_counts}')
    if colony_state.has_lost == True:
        print("Oh no, you lost")
    else:
        print("Yippee, you won!!!!")

if __name__ == "__main__":
    main()
