from pathlib import Path
from collections import deque,defaultdict
from functools import lru_cache
from itertools import combinations
from math import inf as INFINITY
import heapq

with Path('inputs/20.txt').open() as f:
    data = [line.strip('\n') for line in f]

def neighbours(point):
    r,c = point
    nb = []
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        newr,newc = r+dr,c+dc
        if 0 <= newr < len(data) and 0 <= newc < len(data[newr]):
            if data[newr][newc] not in '# ':
                yield (newr,newc)

def portals(point):
    r,c = point
    if data[r][c] != '.':
        return None
    
    isletter = False
    for r1,c1 in neighbours((r,c)):
        letter1 = data[r1][c1]
        if 'A' <= letter1 <= 'Z':
            isletter = True
            break
    if not isletter:
        return None
    for r2,c2 in neighbours((r1,c1)):
        letter2 = data[r2][c2]
        if 'A' <= letter2 <= 'Z':
            break
    
    if r2 > r1 or c2 > c1:
        key = letter1 + letter2
    else:
        key = letter2 + letter1
    
    if r2 == 0 or c2 == 0 or r2 == len(data)-1 or c2 == len(data[0]) -1:
        port = (key,'out', 0)
    else:
        port = (key, 'in', 0)

    return port

def build_graph():
    graph = {}
    for r,row in enumerate(data):
        for c,cell in enumerate(row):
            portal = portals((r,c))
            if portal is not None:
                graph[portal] = find_adj((r,c))

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

            portal = portals(node)
            if portal is not None:
                found.append((portal,dist))
                continue

            for nb in filter(lambda x: x not in visited, neighbours(node)):
                queue.append((dist+1,nb))
    return found


g=build_graph()

# for part 1 only    
for p1, p2 in combinations(g,2):
    if p1[0] == p2[0]:
        g[p1].append((p2,1))
        g[p2].append((p1,1))

def recursive_neighbors(portal):
    depth0_portal    = (portal[0], portal[1], 0)
    depth0_neighbors = g[depth0_portal]
    neighbors = []

    if portal[1] == 'in':
        n = (portal[0], 'out', portal[2] + 1)
        neighbors.append((n, 1))

    if portal[2] == 0:
        for n, d in depth0_neighbors:
            if n[1] == 'in' or n == ('AA','out',0) or n == ('ZZ','out',0):
                neighbors.append((n, d))
    else:
        if portal[1] == 'out':
            n = (portal[0], 'in', portal[2] - 1)
            neighbors.append((n, 1))

        for n, d in depth0_neighbors:
            if n != ('AA','out',0) and n != ('ZZ','out',0):
                n = (n[0], n[1], portal[2])
                neighbors.append((n, d))

    return tuple(neighbors)

def find_path(get_neighbours=None):
    if get_neighbours is None:
        get_neighbours = g.get
    current = ('AA','out',0)
    end = ('ZZ','out',0)
    distance = defaultdict(lambda: INFINITY)
    queue = [(0,current)]
    visited = set()

    distance[current] = 0

    while queue:
        dist, node = heapq.heappop(queue)
        if node == end:
            return dist
        if node not in visited:
            visited.add(node)
            nbors = get_neighbours(node)
            for n,w in filter(lambda x: x[0] not in visited, nbors):
                new_dist = dist + w

                if new_dist < distance[n]:
                    distance[n] == new_dist
                    heapq.heappush(queue,(new_dist,n))
    return None
steps = find_path()
print(steps)
print(find_path(get_neighbours=recursive_neighbors))






