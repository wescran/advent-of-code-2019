from pathlib import Path
from collections import defaultdict
from math import atan2

inputFile = Path("inputs/input-10-01.txt").read_text().rstrip().split()
data = [[char for char in row] for row in inputFile]

asteroids = []
for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] == '#':
            asteroids.append((x,y))
# PART 1
slopes = defaultdict(list)
max_seen = 0
for site in asteroids:
    for asteroid in asteroids:
        dx,dy = asteroid[0]-site[0], asteroid[1]-site[1]
        if dx == 0 and dy == 0:
            continue
        if atan2(dy,dx) in slopes[site]:
            continue
        slopes[site].append(atan2(dy,dx))
    count = len(slopes[site])
    if max_seen == 0:
        max_seen = count
        best = site
    elif count > max_seen:
        max_seen = count
        best = site
print(best, max_seen)

# PART 2
# best is (19,11)
tracked = defaultdict(list)
for asteroid in asteroids:
    dx,dy = asteroid[0]-19, asteroid[1]-11
    if dx == 0 and dy == 0:
        continue
    tracked[atan2(dy,dx)].append((dx,dy))

start = sorted([slope for slope in slopes[best] if slope >= atan2(-1,0)])
end = sorted([slope for slope in slopes[best] if slope < atan2(-1,0)])
start.extend(end)

destroy_count = 0
running = True
while running:
    for slope in start:
        tracked[slope].sort(key = lambda x: abs(x[0]) + abs(x[1]))
        if tracked[slope]:
            destroyed = tracked[slope].pop(0)
            destroy_count += 1
        if destroy_count == 200:
            running = False
            break
print(destroyed, (19 + destroyed[0])*100, (11 + destroyed[1]))
