from pathlib import Path
from collections import deque,defaultdict
from functools import lru_cache
from math import inf as INFINITY
import heapq

tunnels = {}
keys = {}
doors = {}
x,y = 0,0
with Path('inputs/input-18-01.txt').open() as f:
    for line in f:
        for c in line.rstrip():
            tunnels[(x,y)] = c
            if c not in '.#':
                if c == '@':
                    start = (x,y)
                elif c.islower():
                    keys[(x,y)] = c
                else:
                    doors[(x,y)] = c
            x+=1
        x=0
        y+=1

maxx = max(tunnels, key=lambda x: x[0])[0]
maxy = max(tunnels, key=lambda x: x[1])[1]
minx = min(tunnels, key=lambda x: x[0])[0]
miny = min(tunnels, key=lambda x: x[1])[1]

image = [[ tunnels[(x,y)] for x in range(minx,maxx+1)] for y in range(miny,maxy+1)]
for row in image:
    print(*row)

def neighbours(point):
    x,y = point
    nb = []
    for dx,dy in ((0,1),(1,0),(0,-1),(-1,0)):
        newx,newy = x+dx,y+dy
        try:
            c = tunnels[(newx,newy)]
        except KeyError:
            continue
        if c != '#':
            yield (newx,newy)

def build_graph():
    graph = {}
    for pos,val in tunnels.items():
        if val not in '#.':
            graph[val] = find_adj(pos)
    return graph

def find_adj(point):
    queue = deque()
    visited = {point}
    found = []

    for n in neighbours(point):
        queue.append((1,n))

    while queue:
        dist, node = queue.popleft()

        if node not in visited:
            visited.add(node)

            val = tunnels[node]
            if (node in keys or node in  doors) and val not in found:
                found.append((val,dist))
                continue
        for nb in filter(lambda x: x not in visited, neighbours(node)):
            queue.append((dist+1,nb))
    return found

@lru_cache(2**20)
def distance_for_keys(keys):
    return defaultdict(lambda: INFINITY)

@lru_cache(2**20)
def next_keys(pos,found):
    queue = []
    distance = distance_for_keys(found)
    reachable = []

    for nb, weight in g[pos]:
        queue.append((weight,nb))
    heapq.heapify(queue)

    while queue:
        d,n = heapq.heappop(queue)
        if n.islower() and n not in found:
            reachable.append((n,d))
            continue
        if n.lower() not in found:
            continue
        for nb, w in g[n]:
            new_dist = d + w

            if new_dist < distance[nb]:
                distance[nb] = new_dist
                heapq.heappush(queue,(new_dist,nb))
    return reachable

@lru_cache(2**20)
def get_steps(sources,need,found=frozenset()):
    if need == 0:
        return 0
    best = INFINITY
    for src in sources:
        for pos,dist in next_keys(src,found):
            newsources = sources.replace(src,pos)
            new_found = found | {pos}
            new_dist = dist

            new_dist += get_steps(newsources,need-1,new_found)

            if new_dist < best:
                best = new_dist

    return best


g=build_graph()

min_steps = get_steps('@',26)
print(min_steps)

for x,y in neighbours(start):
    tunnels[(x,y)] = '#'
a,b = start
tunnels[start] = '#'
tunnels[(a-1,a-1)] = '1'
tunnels[(a+1,a-1)] = '2'
tunnels[(a+1,a+1)] = '3'
tunnels[(a-1,a+1)] = '4'

distance_for_keys.cache_clear()
next_keys.cache_clear()
get_steps.cache_clear()

g = build_graph()
min_steps_2 = get_steps('1234', 26)
print(min_steps_2)
