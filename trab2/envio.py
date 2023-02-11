from argparse import ArgumentParser
import sys
import re

restrictions = []
current_sol = None
items_weight = None
problem_params = None

from typing import List, Tuple

def bin_packing(n: int, items: List[Tuple[int, int]], C: int, constraints: List[Tuple[int, int]]) -> List[List[int]]:
    def bound(level: int, trips: List[List[int]]) -> int:
        # calculate the remaining weight that can be packed in trips
        remaining = C
        for trip in trips:
            remaining -= sum([items[item][1] for item in trip])
        # add items to trips to get the maximum number of trips required
        level = len(trips[-1]) if trips else 0
        while level < n and items[level][1] <= remaining:
            remaining -= items[level][1]
            level += 1
        return len(trips) + (n - level + len(trips) - 1) // len(trips) + 1
    
    def backtrack(level: int, trips: List[List[int]]) -> bool:
        weight = 0
        if not trips:
            weight = 0
        else:
            for item in trips[-1]: 
                for item_index, item_weight in items:
                    if item_index == item: 
                        weight += item_weight
        if weight > C:
            # if weight exceeds the capacity, return False
            return False
        if level == n:
            # if all items have been packed, return True
            return True
        item = items[level][0]
        # try packing the current item in each trip
        for trip in trips:
            if item not in trip:
                # check if the constraints are satisfied
                constraints_satisfied = True
                for (a, b) in constraints:
                    if (a in trip and b == item) or (b in trip and a == item):
                        constraints_satisfied = False
                        break
                if constraints_satisfied:
                   
                    trip.append(item)
                    if backtrack(level + 1, trips):
                        return True
                    trip.pop()
        # create a new trip if the current item cannot be packed in any existing trip
        trips.append([item])
        if backtrack(level + 1, trips):
            return True
        trips.pop()
        # use branch and bound to prune the search space
        if bound(level + 1, trips) >= len(trips):
            return False
        return backtrack(level + 1, trips)
    
    items = sorted(items, key=lambda x: x[1], reverse=True)
    trips = []
    backtrack(0, trips)
    return trips


argument_parser = ArgumentParser() 
argument_parser.add_argument("-f", help="With the -f option on the command line it must turn off the feasibility cuts", action="store_true", default=False)
argument_parser.add_argument("-o", help="With the -f option on the command line it must turn off the optimally cuts", action="store_true", default=False)
argument_parser.add_argument("-a", help="with the -a option on the command line it must use the given limiting function by teacher", action="store_true", default=False)

args = argument_parser.parse_args()

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

print()
print([tuple(x) for x in restrictions])

print(bin_packing(len(items_weight), list(zip(range(0, len(items_weight)), items_weight)), problem_params[2], [tuple(x) for x in restrictions]))

# print(current_sol)
