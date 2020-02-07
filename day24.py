from pathlib import Path
from collections import defaultdict,deque,Counter
from netcode import intcode
from itertools import chain,product
from copy import copy, deepcopy

with Path('inputs/24.txt').open() as f:
    data = [[c for c in l.strip()] for l in f]
#data = ['....#', '#..#.', '#..##', '..#..', '#....']
def neighbors(level,tile):
    r,c = tile
    adj_bug,adj_empty = 0,0
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        newr,newc = r+dr,c+dc
        if 0 <= newr < 5 and 0 <= newc < 5:
            val = level[newr][newc]
            if val == '#':
                adj_bug += 1
    return adj_bug

def biodiversity(string):
    rating = 0
    for i,tile in enumerate(string):
        if tile == '#':
            rating += 2**i
    return rating

def recursive_find(level,outer,inner,tile):
    r,c = tile
    adj_bug = 0

    if outer is not None:
        if c == 0 and outer[2][1] == '#':
            adj_bug += 1
        if r == 0 and outer[1][2] == '#':
            adj_bug += 1
        if c == 4 and outer[2][3] == '#':
            adj_bug += 1
        if r == 4 and outer[3][2] == '#':
            adj_bug += 1

    if inner is not None:
        if (r,c) == (2,1):
            adj_bug += sum(inner[i][0] == '#' for i in range(5))
        elif (r,c) == (1,2):
            adj_bug += sum(inner[0][i] == '#' for i in range(5))
        elif (r,c) == (2,3):
            adj_bug += sum(inner[i][4] == '#' for i in range(5))
        elif (r,c) == (3,2):  
            adj_bug += sum(inner[4][i] == '#' for i in range(5))

    adj_bug += neighbors(level,(r,c))
    if level[r][c] == '#':
        if adj_bug != 1:
            return  '.'
        return  '#'
    else:
        if adj_bug == 1 or adj_bug == 2:
            return '#'
        return '.'

def next_level(levels,depth):
    if depth in levels:
        level = levels[depth]
    else:
        level = [['.']*5 for _ in range(5)]

    new_level = [['.']*5 for _ in range(5)]
    outer = levels.get(depth+1)
    inner = levels.get(depth-1)

    for r,c in product(range(5),range(5)):
        if (r,c) == (2,2):
            continue
        new_level[r][c] = recursive_find(level,outer,inner,(r,c))
    return new_level

def part1():
    while True:
        layer = []
        string = ''
        for r,row in enumerate(data):
            layer.append([])
            for c,col in enumerate(row):
                bugs = recursive_find(outer,lower,(r,c))
                if col == '#':
                    if bugs != 1:
                        layer[r].append('.')
                    else:
                        layer[r].append('#')
                if col == '.':
                    if bugs == 1 or bugs == 2:
                        layer[r].append('#')
                    else:
                        layer[r].append('.')
            string += ''.join(layer[r])
        if string in seen:
            res = biodiversity(string)
            running = False
            break
        else:
            seen.add(string)
        data = layer
        time += 1

#seen = set()
#seen.add(''.join(data))

levels = {}
levels[0] = deepcopy(data)

min_depth,max_depth = 0,0
for _ in range(200):
    new_levels = {}

    for depth in levels:
        new_levels[depth] = next_level(levels,depth)

    min_depth -= 1
    new_levels[min_depth] = next_level(levels,min_depth)

    max_depth += 1
    new_levels[max_depth] = next_level(levels,max_depth)

    levels = new_levels

bugs = sum(sum(sum(c == '#' for c in row) for row in level) for level in levels.values())

print(bugs)
