from pathlib import Path
from collections import defaultdict

inputFile = Path("inputs/input-03-01.txt")

with inputFile.open() as f:
    data1 = f.readline().rstrip().split(",")
    data2 = f.readline().rstrip().split(",")

# Part 1
# start at 0,0 and trace route of first line, recording coordinates in dict
trace = defaultdict(list)
x,y = 0,0
for route in data1:
    xprev = x
    yprev = y
    if route.startswith('R'):
        x += int(route[1:])
    elif route.startswith('L'):
        x -= int(route[1:])
    elif route.startswith('U'):
        y += int(route[1:])
    elif route.startswith('D'):
        y -= int(route[1:])

    if abs(x - xprev) > 0:
        if x < 0:
            for i in range(xprev,x,-1):
                trace[(i - 1, yprev)].append(1)
        elif x > 0:
            for i in range(xprev,x):
                trace[(i + 1, yprev)].append(1)
    elif abs(y - yprev) > 0:
        if y < 0:
            for i in range(yprev,y, -1):
                trace[(xprev, i - 1)].append(1)
        if y > 0:
            for i in range(yprev,y):
                trace[(xprev, i + 1)].append(1)
    #print(xprev,yprev,x,y)
x,y,best = 0,0,0
for route in data2:
    xprev = x
    yprev = y
    if route.startswith('R'):
        x += int(route[1:])
    elif route.startswith('L'):
        x -= int(route[1:])
    elif route.startswith('U'):
        y += int(route[1:])
    elif route.startswith('D'):
        y -= int(route[1:])
    
    if abs(x - xprev) > 0:
        if x < 0:
            for i in range(xprev,x,-1):
                if 1 in trace[(i - 1, yprev)]:
                    dist = abs(i - 1) + abs(yprev)
                    if best == 0:
                        best = dist
                    elif dist < best:
                        best = dist 
        if x > 0:
            for i in range(xprev,x):
                if 1 in trace[(i + 1, yprev)]:
                    dist = abs(i + 1) + abs(yprev)
                    if best == 0:
                        best = dist
                    elif dist < best:
                        best = dist 
    elif abs(y - yprev) > 0:
        if y < 0:
            for i in range(yprev,y, -1):
                if 1 in trace[(xprev, i - 1)]:
                    dist = abs(xprev) + abs(i - 1)
                    if best == 0:
                        best = dist
                    elif dist < best:
                        best = dist 
        if y > 0:
            for i in range(yprev,y):
                if 1 in trace[(xprev, i + 1)]:
                    dist = abs(xprev) + abs( i + 1)
                    if best == 0:
                        best = dist
                    elif dist < best:
                        best = dist 
print(best)
'''
# Part 2
# start at 0,0 and trace route of first line, recording coordinates in dict
trace = defaultdict(list)
x,y,steps = 0,0,0
for route in data1:
    xprev = x
    yprev = y
    sprev = steps
    if route.startswith('R'):
        x += int(route[1:])
    elif route.startswith('L'):
        x -= int(route[1:])
    elif route.startswith('U'):
        y += int(route[1:])
    elif route.startswith('D'):
        y -= int(route[1:])
    steps += int(route[1:])

    if x - xprev < 0:
        for i in range(xprev,x,-1):
            trace[(i - 1, yprev)].append((1, sprev + xprev - i + 1))
    elif x - xprev > 0:
        for i in range(xprev,x):
            trace[(i + 1, yprev)].append((1, sprev + i + 1 - xprev))
    elif y - yprev < 0:
        for i in range(yprev,y, -1):
            trace[(xprev, i - 1)].append((1, sprev + yprev - i + 1))
    elif y - yprev > 0:
        for i in range(yprev,y):
            trace[(xprev, i + 1)].append((1, sprev + i + 1 - yprev))

x,y,best,steps,add_steps = 0,0,0,0,0
for route in data2:
    xprev = x
    yprev = y
    sprev = steps
    if route.startswith('R'):
        x += int(route[1:])
    elif route.startswith('L'):
        x -= int(route[1:])
    elif route.startswith('U'):
        y += int(route[1:])
    elif route.startswith('D'):
        y -= int(route[1:])
    steps += int(route[1:])
    if x-xprev < 0:
        for i in range(xprev,x,-1):
            try:
                tup = trace[(i - 1, yprev)][0]
            except IndexError:
                continue
            if tup[0] == 1:
                add_steps = tup[1] + sprev + xprev - i + 1
                if best == 0:
                    best = add_steps
                elif add_steps < best:
                    best = add_steps
    elif x-xprev > 0:
        for i in range(xprev,x):
            try:
                tup = trace[(i + 1, yprev)][0]
            except IndexError:
                continue
            if tup[0] == 1:
                add_steps = tup[1] + sprev + i + 1 - xprev
                if best == 0:
                    best = add_steps
                elif add_steps < best:
                    best = add_steps 
    elif y-yprev < 0:
        for i in range(yprev,y, -1):
            try:
                tup = trace[(xprev, i - 1)][0]
            except IndexError:
                continue
            if tup[0] == 1:
                add_steps = tup[1] + sprev + yprev - i + 1
                if best == 0:
                    best = add_steps
                elif add_steps < best:
                    best = add_steps 
    elif y-yprev > 0:
        for i in range(yprev,y):
            try:
                tup = trace[(xprev, i + 1)][0]
            except IndexError:
                continue
            if tup[0] == 1:
                add_steps = tup[1] + sprev + i + 1 - yprev
                if best == 0:
                    best = add_steps
                elif add_steps < best:
                    best = add_steps
print(best)
'''
