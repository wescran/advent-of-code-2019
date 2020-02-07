from pathlib import Path
from collections import defaultdict
# north(1), south(2), west(3), east(4)
# 0 hit a wall
# 1 moved one step
# 2 moved one step, position is at oxygen tank
inputFile = Path("inputs/input-15-01.txt").read_text().split(",")
data = [int(i) for i in inputFile]

path = defaultdict(int)

def extend_mem(data_length, new_add):
    return [0 for _ in range(data_length,new_add)]

def intcode():
    num,base = 0,0
    while True:
        # make sure all instrctions are of length 4
        inst = str(data[num])
        if len(inst) < 5:
            inst = '0'*(5-len(inst)) + inst
        
        # these are for opcodes that have 2 or less params    
        if inst[-2:] == '03':
            inputNum = yield
            if inst[-3] == '0':
                data[data[num+1]] = inputNum 
            else:
                data[data[num+1] + base] = inputNum
            num += 2
            continue
        elif inst[-2:] == '04':
            if inst[-3] == '0':
                val = data[data[num+1]]
            elif inst[-3] == '1':
                val = data[num+1]
            else:
                val = data[data[num+1] + base]
            num += 2
            yield val
        elif inst[-2:] == '09':
            if inst[-3] == '0':
                val = data[data[num+1]]
            elif inst[-3] == '1':
                val = data[num+1]
            else:
                val = data[data[num+1] + base]
            base = base + val  
            num += 2
            continue
        elif inst[-2:] == '99':
            running = False
            print('Done')
            break
        
        # this part for instructions with more than 2 params
        # param 1
        if inst[-3] == '0':
            try:
                par1 = data[data[num+1]]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+1] +1)])
                par1 = data[data[num+1]]
        elif inst[-3] == '1':
            try:
                par1 = data[num+1]
            except IndexError:
                data.extend([0 for _ in range(len(data), num+1 +1)])
                par1 = data[num+1]
        else:
            try:
                par1 = data[data[num+1] + base]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+1] +base +1)])
                par1 = data[data[num+1] + base]

        # param 2
        if inst[-4] == '0':
            try:
                par2 = data[data[num+2]]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+2] +1)])
                par2 = data[data[num+2]]
        elif inst[-4] == '1':
            try:
                par2 = data[num+2]
            except IndexError:
                data.extend([0 for _ in range(len(data), num+2 +1)])
                par2 = data[num+2]
        else:
            try:
                par2 = data[data[num+2] + base]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+2]+base +1)])
                par2 = data[data[num+2] + base]

        if inst[-2:] == '01':
            val = par1 + par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3] +1)])
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                    data[data[num+3] + base] = val
        elif inst[-2:] == '02':
            val = par1 * par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3] +1)])
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                    data[data[num+3] + base] = val
        elif inst[-2:] == '05':
            if par1 != 0:
                num = par2
                continue
            num += 3
            continue
        elif inst[-2:] == '06':
            if par1 == 0:
                num = par2
                continue
            num +=3
            continue
        elif inst[-2:] == '07':
            if par1 < par2:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
        elif inst[-2:] == '08':
            if par1 == par2:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
        num += 4
previous = defaultdict(list)
move = {1:"N", 2:"S", 3:"W", 4:"E"}
opps = {"N":2, "S":1, "W":4, "E":3} 
dirs = {"N":(0,1),"S":(0,-1),"W":(-1,0),"E":(1,0)}
count,x,y,prevx,prevy = 0,0,0,0,0
running = True
remove = None
nums = {}
nums[(0,0)] = [1,2,3,4]
while running:
    try:
        nums[(x,y)]
    except KeyError:
        nums[(x,y)] = [1,2,3,4]
    if remove in nums[(x,y)]:
        nums[(x,y)].pop(nums[(x,y)].index(remove))
        remove = None
    try:
        num = nums[(x,y)].pop(0)
    except IndexError:
        num = previous[(x,y)].pop(0)
        #x += dirs[move[num]][0]
        #y += dirs[move[num]][1]

    prog = intcode()
    next(prog)
    res = prog.send(num)
    dx,dy = dirs[move[num]]
    #print(res,num,(x,y),nums[(x,y)],(dx,dy))
    if res == 0:
        path[(x+dx,y+dy)] = "#"
        continue
    elif res == 1:
        path[(x,y)] = "."
        xprev,yprev = x,y
        x+=dx
        y+=dy
        previous[(x,y)].append(opps[move[num]])
        if path[(x,y)] == ".":
            count -= 1
        else:
            count += 1
        remove = opps[move[num]]
    elif res == 2:
        path[(x,y)] = "."
        xprev,yprev = x,y
        x+=dx
        y+=dy
        path[(x,y)] = "O"
        end = (x,y)
        count += 1
        running = False


maxx = max(path, key=lambda x: x[0])[0]
maxy = max(path, key=lambda x: x[1])[1]
minx = min(path, key=lambda x: x[0])[0]
miny = min(path, key=lambda x: x[1])[1]

image = [[ path[(x,y)] for x in range(minx,maxx+1)] for y in range(maxy,miny-1,-1)]
for row in image:
    print(*row)
print(count,end)

levels = [[end]]
minutes = 0
while True:
    level = levels.pop(0)
    #print(level)
    for tile in level:
        for dx,dy in dirs.values():
            x,y = tile
            x,y = x + dx, y + dy
            #print(x,y, path[(x,y)])
            if path[(x,y)] == ".":
                path[(x,y)] = "O"
                if levels == []:
                    levels.append([])
                levels[-1].append((x,y))
    if levels == []:
        break
    minutes += 1
print(minutes)
image = [[ path[(x,y)] for x in range(minx,maxx+1)] for y in range(maxy,miny-1,-1)]
for row in image:
    print(*row)
