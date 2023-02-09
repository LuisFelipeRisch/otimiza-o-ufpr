from argparse import ArgumentParser
import sys
import re

argument_parser = ArgumentParser() 
argument_parser.add_argument("-f", help="With the -f option on the command line it must turn off the feasibility cuts", action="store_false", default=True)
argument_parser.add_argument("-o", help="With the -f option on the command line it must turn off the feasibility cuts", action="store_false", default=True)
argument_parser.add_argument("-a", help="with the -a option on the command line it must use the given limiting function by teacher", action="store_true", default=False)

args = argument_parser.parse_args()

restrictions = []
items_weight = None
quantity_vars = None

for line in sys.stdin:
    line = line.strip()
    line =  re.sub(r'\s+', ' ', line)
    splitted_line = line.split(" ")
    splitted_line = list((map(int, splitted_line)))

    if quantity_vars == None:
        quantity_vars = splitted_line
    elif items_weight == None:
        items_weight = splitted_line
    else:
        restrictions.append(splitted_line)

print(quantity_vars)
print(items_weight)
print(restrictions)
