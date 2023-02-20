from argparse import ArgumentParser
from typing import List, Tuple
import sys
import math
import re
import copy
import time

total_nodes = 0
best_trips_qnt = math.inf
best_trips_arrangement = None

def print_result(n):
    for item in range(n):
        for index, trip in enumerate(best_trips_arrangement):
            if item in trip:
                sys.stdout.write(f'{index + 1}')
                break
        if item != n - 1:
            sys.stdout.write(" ")
    sys.stdout.write(f'\n{best_trips_qnt}')

def print_log(problem_params:List[int], item_weights:List[int], restrictions:List[int], total_time_sec:float):
    sys.stderr.write(f'n = {problem_params[0]}; p = {problem_params[1]}; c = {problem_params[2]}\n')

    for item in range(len(item_weights)):
        sys.stderr.write(f'O item {item + 1} tem a massa de {item_weights[item]}\n')

    for restriction in restrictions:
        sys.stderr.write(f'O item {restriction[0]} não pode viajar junto com o {restriction[1]}\n')

    sys.stderr.write(f'O branch and bound levou {total_time_sec:0.4f} segundos para ser executado e a árvore gerada teve um total de {total_nodes} nodos\n')

def bin_packing(weights:List[int], MAX_CAPACITY:int, constrains: List[Tuple[int, int]], should_use_teachers_bound:bool, should_turn_off_feasibility_cuts:bool, should_turn_off_optimally_cuts:bool) -> None:
    # In order to active it, just do not pass the argument -a when executing program
    def my_bound(trips:List[List[int]]) -> float:
        for trip in trips:
            if trip != sorted(trip):
                return True
        return False

    # In order to active it, just pass the argument -a when executing program
    def teachers_bound(trips:List[List[int]]) -> float:
        return max(len(trips), sum(weights) / MAX_CAPACITY) >= best_trips_qnt

    def should_prune(trips:List[List[int]]) -> bool:
        if not should_turn_off_optimally_cuts:
            if should_use_teachers_bound:
                if teachers_bound(trips):
                    return True
            else:
                if my_bound(trips):
                    return True
        return False

    def branch_and_bound(start:bool, available_items:List[int], trips:List[List[int]]) -> None:
        global best_trips_arrangement, best_trips_qnt, total_nodes
        total_nodes += 1

        if start:
            for item in available_items:
                branch_and_bound(False, [x for x in available_items if x != item], [[item]])
        else:
            if len(available_items) == 0:
                if should_turn_off_feasibility_cuts:
                    is_feasible = True

                    for trip in trips:
                        current_weight = 0
                        for item in trip:
                            current_weight += weights[item]

                        if current_weight > MAX_CAPACITY:
                            is_feasible = False
                            break

                        for (a, b) in constrains:
                            if a in trip and b in trip:
                                is_feasible = False
                                break

                    if is_feasible:
                        best_trips_qnt = len(trips)
                        best_trips_arrangement = copy.deepcopy(trips)
                else:
                    if len(trips) < best_trips_qnt:
                        best_trips_qnt = len(trips)
                        best_trips_arrangement = copy.deepcopy(trips)
            else:
                for current_item in available_items:
                    found = False
                    trips_copied = copy.deepcopy(trips)

                    for trip in trips_copied:
                        if should_turn_off_feasibility_cuts:
                            trip.append(current_item)
                            found = True
                            break
                        else:
                            if current_item not in trip:
                                constraints_satisfied = True
                                for (a, b) in constrains:
                                    if (a in trip and b == current_item) or (b in trip and a == current_item):
                                        constraints_satisfied = False
                                        break

                                if not constraints_satisfied:
                                    continue

                                current_weight = 0
                                for item in trip:
                                    current_weight += weights[item]
                                current_weight += weights[current_item]

                                if constraints_satisfied and current_weight <= MAX_CAPACITY:
                                    trip.append(current_item)
                                    found = True
                                    break

                    if not found:
                        trips_copied.append([current_item])

                    if should_prune(trips_copied):
                        continue

                    branch_and_bound(False, [x for x in available_items if x != current_item], trips_copied)

    branch_and_bound(True, [*range(len(weights))], [[]])

argument_parser = ArgumentParser()
argument_parser.add_argument("-f", help="With the -f option on the command line it must turn off the feasibility cuts", action="store_true", default=False)
argument_parser.add_argument("-o", help="With the -o option on the command line it must turn off the optimally cuts", action="store_true", default=False)
argument_parser.add_argument("-a", help="with the -a option on the command line it must use the given limiting function by teacher", action="store_true", default=False)

args = argument_parser.parse_args()

should_turn_off_feasibility_cuts = args.f
should_turn_off_optimally_cuts = args.o
should_use_teachers_bound = args.a

restrictions = []
items_weight = None
problem_params = None

for line in sys.stdin:
    line = line.strip()
    line =  re.sub(r'\s+', ' ', line)
    splitted_line = line.split(" ")
    splitted_line = list((map(int, splitted_line)))

    if problem_params == None:
        problem_params = splitted_line
    elif items_weight == None:
        items_weight = splitted_line
    else:
        restrictions.append([x - 1 for x in splitted_line])

start_time = time.perf_counter()
bin_packing(items_weight, problem_params[2], [tuple(x) for x in restrictions], should_use_teachers_bound, should_turn_off_feasibility_cuts, should_turn_off_optimally_cuts)
end_time = time.perf_counter()

print(best_trips_qnt)
print(best_trips_arrangement)

# print_result(len(items_weight))
# print_log(problem_params, items_weight, restrictions, end_time - start_time)