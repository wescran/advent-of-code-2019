from pathlib import Path
from collections import defaultdict
# robot starts up, all panels black
# input is 0 if black, 1 if white
# 1. 0=black, 1=white
# 2. 0=left 90, 1=right 90
inputFile = Path("inputs/input-11-01.txt").read_text().split(",")
data = [int(i) for i in inputFile]
num,base,x,y= 0,0,0,0
direction = "U"
panels = defaultdict(int)
painted = []

def extend_mem(data_length, new_add):
    return [0 for _ in range(data_length,new_add)]

def move(turn,direction):
    right = {"U":"R", "R":"D", "D":"L", "L":"U"}
    left = {"U":"L", "L":"D", "D":"R", "R":"U"}

    movement = {"U":(0,1),"R":(1,0),"D":(0,-1),"L":(-1,0)}

    if turn == 0:
        return left[direction],movement[left[direction]]
    elif turn == 1:
        return right[direction],movement[right[direction]]
panels[(x,y)] = 1
running = True
while running:
    nextout = False
    inputNum = panels[(x,y)]
    while True:
        # make sure all instrctions are of length 4
        inst = str(data[num])
        if len(inst) < 5:
            inst = '0'*(5-len(inst)) + inst
        
        # these are for opcodes that have 2 or less params    
        if inst[-2:] == '03':
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
            if nextout:
                turn = val
                nextout = False
                break
            else:
                color = val
                nextout = True
                continue
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
            break
        
        # this part for instructions with more than 2 params
        # param 1
        if inst[-3] == '0':
            try:
                par1 = data[data[num+1]]
            except IndexError:
                data.extend(extend_mem(len(data), data[num+1] +1))
                par1 = data[data[num+1]]
        elif inst[-3] == '1':
            try:
                par1 = data[num+1]
            except IndexError:
                data.extend(extend_mem(len(data), num+1 +1))
                par1 = data[num+1]
        else:
            try:
                par1 = data[data[num+1] + base]
            except IndexError:
                data.extend(extend_mem(len(data), data[num+1]+base +1))
                par1 = data[data[num+1] + base]

        # param 2
        if inst[-4] == '0':
            try:
                par2 = data[data[num+2]]
            except IndexError:
                data.extend(extend_mem(len(data), data[num+2] +1))
                par2 = data[data[num+2]]
        elif inst[-4] == '1':
            try:
                par2 = data[num+2]
            except IndexError:
                data.extend(extend_mem(len(data), num+2 +1))
                par2 = data[num+2]
        else:
            try:
                par2 = data[data[num+2] + base]
            except IndexError:
                data.extend(extend_mem(len(data), data[num+2]+base +1))
                par2 = data[data[num+2] + base]

        if inst[-2:] == '01':
            val = par1 + par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend(extend_mem(len(data), data[num+3] + 1))
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend(extend_mem(len(data), data[num+3] + base + 1))
                    data[data[num+3] + base] = val
        elif inst[-2:] == '02':
            val = par1 * par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend(extend_mem(len(data), data[num+3] + 1))
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend(extend_mem(len(data), data[num+3] + base + 1))
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
                        data.extend(extend_mem(len(data), data[num+3] + 1))
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + base + 1))
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + 1))
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + base + 1))
        elif inst[-2:] == '08':
            if par1 == par2:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 1
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + 1))
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + base + 1))
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + 1))
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend(extend_mem(len(data), data[num+3] + base + 1))
        num += 4

    if color == 0:
        panels[(x,y)] = 0
    else:
        panels[(x,y)] = 1
    
    if (x,y) not in painted:
        painted.append((x,y))

    direction, movement = move(turn,direction)
    x, y = x+movement[0], y+movement[1]
print(len(painted))
print(max(panels, key=lambda x: x[0])[0], min(panels, key=lambda x: x[1]))

image = [["1" if panels[(x,y)] == 1 else " " for x in range(43)] for y in range(0,-6,-1)]

for row in image:
    print(*row)
