from pathlib import Path
from collections import defaultdict
from intcode import intcode
from itertools import chain

inputFile = Path('inputs/input-17-01.txt').read_text().rstrip().split(",")

data = [int(_) for _ in inputFile]

camera = {}
codes = {10:'L', 35:'#', 46:'.', 60:'<', 62:'>', 86:'v', 94:'^'}
prog = intcode(data)
x,y = 0,0

while True:
    try:
        num = next(prog)
    except StopIteration:
        break
    if codes[num] == 'L':
        x = 0
        y += 1
        continue
    camera[(x,y)] = codes[num]
    x+=1
params,intersections = 0,0
for tile,val in camera.items():
    if val in '<>v^':
        print('start:',tile)
    elif val != '#':
        continue
    x,y = tile
    try:
        if all((v == '#' for v in [camera[(x,y+1)],camera[(x,y-1)],camera[(x+1,y)],camera[(x-1,y)]])):
            params += x*y
    except KeyError:
        continue
maxx = max(camera, key=lambda x: x[0])[0]
maxy = max(camera, key=lambda x: x[1])[1]
minx = min(camera, key=lambda x: x[0])[0]
miny = min(camera, key=lambda x: x[1])[1]

image = [[ camera[(x,y)] for x in range(minx,maxx+1)] for y in range(miny,maxy+1)]
for row in image:
    print(*row)
print(params,intersections)

data = [int(_) for _ in inputFile]
data[0] = 2
x,y = (84,18) #facing N
cur_dir = 'S'
left = {'N':'W','W':'S','S':'E','E':'N'}
right = {'N':'E','E':'S','S':'W','W':'N'}
move = {'N':(0,1),'E':(-1,0),'S':(0,-1),'W':(1,0)}
steps = 0
path = []
while True:
    dx,dy = move[cur_dir]
    newx,newy = x+dx,y+dy

    try:
        if camera[(newx,newy)] == '#':
            steps += 1
            x,y = newx,newy
            continue
    except KeyError:
        pass
        
    new_dir = left[cur_dir]
    dx,dy = move[new_dir]
    newx,newy = x+dx,y+dy

    try:
        if camera[(newx,newy)] == '#':
            turn = 'L'
            x,y = newx,newy
            cur_dir = new_dir
            if steps > 0:
                path.append(str(steps))
            path.append(turn)
            steps = 1
            continue
    except KeyError:
        pass

    new_dir = right[cur_dir]
    dx,dy = move[new_dir]
    newx,newy = x+dx,y+dy
    
    try:
        if camera[(newx,newy)] == '#':
            turn = 'R'
            x,y = newx,newy
            cur_dir = new_dir
            if steps > 0:
                path.append(str(steps))
            path.append(turn)
            steps = 1
            continue
    except KeyError:
        pass
    path.append(str(steps))
    break
routine = [ ord(r) for r in 'A,B,A,B,C,C,B,A,B,C\n']
func_a = [ ord(a) for a in ','.join(path[:8]) + '\n']
func_b = [ ord(b) for b in ','.join(path[8:14]) + '\n']
func_c = [ ord(c) for c in ','.join(path[-6:])+ '\n']
prompt = [ ord(p) for p in 'n\n']

prog = intcode(data)
ins = chain(routine,func_a,func_b,func_c,prompt)
prog = intcode(data, list(ins))
while True:
    try:
        res = next(prog)
    except StopIteration:
        break
print(res)
