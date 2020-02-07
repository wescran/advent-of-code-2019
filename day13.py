from pathlib import Path
from collections import defaultdict
# robot starts up, all panels black
# input is 0 if black, 1 if white
# Wall and Paddle are not
# Block is destructible
inputFile = Path("inputs/input-13-01.txt").read_text().split(",")
data = [int(i) for i in inputFile]
num,base,dx,dy,tile = 0,0,0,0,0
data[0] = 2

for i in range(len(data)-2):
    if data[i] == 0 and data[i+1] == 3 and data[i+2] == 0:
        ball = i+1
        break
print(ball)
for r in range(ball-17,ball + 18):
    data[r] = 1


board = defaultdict(int)

def extend_mem(data_length, new_add):
    return [0 for _ in range(data_length,new_add)]

tiles = {0:" ", 1:"W", 2:"B", 3:"P", 4:"*"}
running = True
while running:
    out1,out2 = False,False
    while True:
        # make sure all instrctions are of length 4
        inst = str(data[num])
        if len(inst) < 5:
            inst = '0'*(5-len(inst)) + inst
        
        # these are for opcodes that have 2 or less params    
        if inst[-2:] == '03':
            if inst[-3] == '0':
                data[data[num+1]] = 0
            else:
                data[data[num+1] + base] = 0
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
            if out2:
                tile = val
                out2 = False
                out1 = False
                break
            elif out1:
                dy = val
                out1 = False
                out2 = True
                continue
            else:
                dx = val
                out1 = True
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
    if dx == -1 and dy == 0:
        score = tile
    elif tiles[tile] == "*":
        if board[(dx,dy)] != ("W" and "P"):
            board[(dx,dy)] = tiles[tile]
    else:
        board[(dx,dy)] = tiles[tile]

blocks_left = sum(block == "B" for block in board.values())
print(blocks_left, score)
print(max(board, key=lambda x: x[0])[0], max(board, key=lambda x: x[1])[1])

image = [[ board[(x,abs(y))] for x in range(37)] for y in range(0,-22,-1)]
for row in image:
    print(*row)

#573 00204
