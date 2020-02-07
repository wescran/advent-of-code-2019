from pathlib import Path

inputFile = Path("inputs/input-09-01.txt").read_text().split(",")
data = [int(i) for i in inputFile]
num,base,inputNum = 0,0,2

def extend_mem(data_length, new_add):
    return [0 for _ in range(data_length,new_add)]

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
        print(val)
        num += 2
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
        break
    
    # this part for instructions with more than 2 params
    # param 1
    if inst[-3] == '0':
        par1 = data[data[num+1]]
    elif inst[-3] == '1':
        par1 = data[num+1]
    else:
        par1 = data[data[num+1] + base]
    # param 2
    if inst[-4] == '0':
        par2 = data[data[num+2]]
    elif inst[-4] == '1':
        par2 = data[num+2]
    else:
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
