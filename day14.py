from pathlib import Path
from collections import defaultdict
import re
reactions = defaultdict(list)
units = defaultdict(int)
agent = defaultdict(list)
need = defaultdict(int)
have = defaultdict(int)
inputFile = Path("inputs/input-14-01.txt").read_text().rstrip().split("\n")
rx = r"(.*) => (\d+ \w+)"
for reaction in inputFile:
    match = re.match(rx,reaction)
    prod = match.group(2).split(" ")
    reactions[prod[1]].extend([(int(m.split(" ")[0]),m.split(" ")[1]) for m in match.group(1).split(", ")])
    units[prod[1]] += int(prod[0])

def multiple_needed(mult,name):
    mult_in = name[0]*mult - have[name[1]]
    have[name[1]] = 0
    mult_out = units[name[1]]
    d,m = divmod(mult_in,mult_out)
    if m != 0:
        have[name[1]] = mult_out - m
        return d + 1
    else:
        return d

def get_ore(mult,name):
    if name[1] == 'ORE':
        return name[0]*mult
    next_mult = multiple_needed(mult,name)
    ore = 0
    for compound in reactions[name[1]]:
        ore += get_ore(next_mult,compound)
    return ore

mult = 1
name = (1,'FUEL')
part1 = get_ore(mult,name)
print(part1)

ore_total = 1000000000000
fuel_est = ore_total // part1
print(fuel_est)
fuel = 0
have = defaultdict(int)
while ore_total and fuel_est:
    ore_used = get_ore(fuel_est,name)
    if ore_used > ore_total:
        fuel_est //= 2
    else:
        fuel += fuel_est
        ore_total -= ore_used
print(fuel)
