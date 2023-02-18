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

def bin_packing(weights:List[int], MAX_CAPACITY:int, constrains: List[Tuple[int, int]], should_use_teachers_bound:bool, should_turn_off_feasibility_cuts:bool, should_turn_off_optimally_cuts:bool) -> None:
    global best_trips_arrangement, best_trips_qnt, total_nodes

    def my_bound(trips:List[List[int]]) -> float:
        # print("My bound")
        return -math.inf

    def teachers_bound(trips:List[List[int]]) -> float:
        # print("Teachers bound")
        return max(len(trips), sum(weights) / MAX_CAPACITY)

    def branch_and_bound(start:bool, available_items:List[int], trips:List[List[int]]) -> None:
        global best_trips_arrangement, best_trips_qnt, total_nodes
        total_nodes += 1

        if start:
            for item in available_items:
                branch_and_bound(False, [x for x in available_items if x != item], [[item]])
        else:
            if len(available_items) == 0:
                if len(trips) < best_trips_qnt:
                    best_trips_qnt = len(trips)
                    best_trips_arrangement = copy.deepcopy(trips)
            else:
                for current_item in available_items:
                    found = False
                    trips_copied = copy.deepcopy(trips)

                    for trip in trips_copied:
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

                    if not should_turn_off_optimally_cuts:
                        if should_use_teachers_bound:
                            if teachers_bound(trips) >= best_trips_qnt:
                                return
                        else:
                            if my_bound(trips) >= best_trips_qnt:
                                return

                    branch_and_bound(False, [x for x in available_items if x != current_item], trips_copied)

    branch_and_bound(True, [*range(len(weights))], [[]])
    print(best_trips_qnt)
    print(best_trips_arrangement)


# def bin_packing(n: int, items: List[Tuple[int, int]], C: int, constraints: List[Tuple[int, int]]) -> List[List[int]]:
#     def bound(level: int, trips: List[List[int]]) -> int:
#         # calculate the remaining weight that can be packed in trips
#         remaining = C
#         for trip in trips:
#             remaining -= sum([items[item][1] for item in trip])
#         # add items to trips to get the maximum number of trips required
#         level = len(trips[-1]) if trips else 0
#         while level < n and items[level][1] <= remaining:
#             remaining -= items[level][1]
#             level += 1
#         return len(trips) + (n - level + len(trips) - 1) // len(trips) + 1

#     def backtrack(level: int, trips: List[List[int]]) -> bool:
#         for trip in trips:
#             weight = 0
#             for item in trip:
#                 for item_index, item_weight in items:
#                     if item_index == item:
#                         weight += item_weight
#             if weight > C:
#                 return False

#         if level == n:
#             # if all items have been packed, return True
#             return True
#         item = items[level][0]
#         # try packing the current item in each trip
#         for trip in trips:
#             if item not in trip:
#                 # check if the constraints are satisfied
#                 constraints_satisfied = True
#                 for (a, b) in constraints:
#                     if (a in trip and b == item) or (b in trip and a == item):
#                         constraints_satisfied = False
#                         break
#                 if constraints_satisfied:
#                     trip.append(item)
#                     if backtrack(level + 1, trips):
#                         return True
#                     trip.pop()
#         # create a new trip if the current item cannot be packed in any existing trip
#         trips.append([item])
#         if backtrack(level + 1, trips):
#             return True

#     items = sorted(items, key=lambda x: x[1], reverse=True)
#     trips = []

#     print(problem_params)
#     print(items)
#     print(constraints)

#     backtrack(0, trips)
#     return trips


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

print(problem_params)
print(items_weight)
print(restrictions)

start_time = time.perf_counter()
bin_packing(items_weight, problem_params[2], [tuple(x) for x in restrictions], should_use_teachers_bound, should_turn_off_feasibility_cuts, should_turn_off_optimally_cuts)
end_time = time.perf_counter()

print(f"The branch and bound algorithm took {end_time - start_time:0.4f} seconds and generated {total_nodes} nodes")
# print(current_sol)
